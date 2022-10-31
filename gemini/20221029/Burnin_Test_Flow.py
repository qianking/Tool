import time
import os
import threading
from functools import wraps
from datetime import datetime
import Burnin_Test_Item as Test_Item
from datetime import datetime
import create_log as create_log
from concurrent.futures import ThreadPoolExecutor
from exceptions import Test_Fail, Online_Fail
from Upload_Functions import Upload_FTP, SFIS_Function
from Global_Variable import SingleTone_local, SingleTon_Global
from Log_Dealer import Log_Model
import Generate_Log


ui_lock = threading.Lock()

#region 接入從controller下達的參數
def get_veriable_from_controller(**awags):
    if len(awags):
        config = awags['config']
        G = SingleTon_Global()
        G.VERSION = config['VERSION']
        G.online_function = config['online_function']
        G.config_path = config['config_path']
        G.value_config_path = config['value_config_path']
        G.serial_name = config['serial_name']
        G.test_time = config['test_time']
        G.terminal_comport = config['terminal_comport']
        G.open_station = config['open_station']
        G.ftp_upload_path = config['ftp_upload_path']
        G.op = config['op']
#endregion


#region 送訊息到UI
class UI_Contol():

    def __init__(self, **awags):
        self.signal = awags.get('signal')

    def single_status(self, telnet_port, status):
        """
        改變單一station的狀態
        status: ['fail', 'done']
        """
        ui_lock.acquire()
        if self.signal: 
            self.signal.single_light.emit((telnet_port, status))
        ui_lock.release()

    def all_status(self, color, txt):
        """
        改變全部station的狀態
        color: ['lightgreen', 'red']
        """
        ui_lock.acquire()
        if self.signal: 
            self.signal.set_all_checkbox.emit((color, txt))
        ui_lock.release()

    def error_box(self, title, msg):
        """
        跳出error的 message box
        """
        ui_lock.acquire()
        if self.signal: 
            self.signal.error_msg.emit((title, msg))
        ui_lock.release()

    def test_finish(self):
        """
        測試完成
        """
        ui_lock.acquire()
        if self.signal: 
            self.signal.finish.emit()
        ui_lock.release()
#endregion


class Flow_MetaClass(type):
    def __new__(cls, name, bases, local):
        if len(bases):
            for attr in local:
                value = local[attr]
                if callable(value) and attr != '__init__':
                    local[attr] = Fail_Dealer()(value)
        return super().__new__(cls, name, bases, local)


class Fail_Dealer():

    p = SingleTone_local()

    def __init__(self):
        pass
    
    def error_logger(self):
        if len(self.l['_sys_error_msg']):
            self.l['sys_debug_logger'].debug(f"{self.l['run_times']:-^50}")
            for msg in self.l['_sys_error_msg']:
                self.l['sys_debug_logger'].debug(msg)
        
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            self.l = self.p[threading.get_ident()]
            try: 
                func(*args, **kwargs)

            except Test_Fail:
                """測試錯誤，進入後續處理function"""
                return True  #設定為True代表會繼續下一輪的測試，會先跑到test end function
            
            except Online_Fail:
                return False

            except Exception as ex:
                print(ex)
                print('sys_error_msg:', self.l['_sys_error_msg'])
                self.error_logger()
                """系統錯誤，基本上不應該出現，設定彈窗提示，並且停下來"""
                return False  

            else:
                return True
            finally:
                print('upload_log:', self.l['_upload_data'])
        return decorated


class Flow(metaclass = Flow_MetaClass):
    pass

class mChild(type(Flow), type(Test_Item.Terminal_Server_Test_Item)):
    pass 
       
class TerminalFlow(Flow, Test_Item.Terminal_Server_Test_Item, metaclass = mChild):

    G = SingleTon_Global()

    def __init__(self):
        self.baud = '9600'
        Test_Item.Terminal_Server_Test_Item.__init__(self, port = self.G.terminal_comport, baud = self.baud)  
        

    def Check_ALL_Comport(self):
        """
        確認terminal server和pg的port口是否正常
        """
        self.Check_Comport()
    
    def Terminal_Server_Flow(self):
        """
        terminal server清線
        """
        self.Enter_en_Mode()
        self.Clear_Port_on_Terminal(2, 10)


class Online_Flow(Upload_FTP, SFIS_Function):
    
    p = SingleTone_local()
    G = SingleTon_Global()

    def __init__(self):
        self.l = self.p[threading.get_ident()]

        Upload_FTP.__init__(self, self.G.ftp_upload_path, self.l)
        SFIS_Function.__init__(self, self.G.op, self.l)

        self.l['upload_debug_logger'].debug(f"{self.l['run_times']:-^50}")

    def FTP_Upload(self):
        self.ftb_upload_file(self.l['_ftp_local_path'], self.l['_ftp_remote_path'])

    def SFIS_Check_Route(self):
        if self.G.online_function:
            if not self.l['been_checkroute']:
                self.sfis_checkroute(self.l['_dut_info']['SN'])
                self.l['been_checkroute'] = True

    def SFIS_Get_SN(self):
        if self.G.online_function:
            pass
            
    def SFIS_Upload(self):
        if self.G.online_function:
            if not self.l['been_sfis_upload'] and (len(self.l['_dut_error_code']) or self.l['run_times'] == self.G.total_run_times): #如果有ERROR CODE並且還沒上傳過
                self.l['been_sfis_upload'] = True
                self.sfis_upload(self.l['_dut_info']['SN'], self.l['_dut_error_code'], self.l['_sfis_log'])
    
    
        
    def IPLAS_Upload(self):
        if self.G.online_function:
            if not self.l['_check_route_fail']:
                pass


class mChild(type(Flow), type(Test_Item.Gemini_Test_Item)):
    pass 

class MainFlow(Flow, Test_Item.Gemini_Test_Item, Online_Flow, metaclass = mChild):

    p = SingleTone_local()

    def __init__(self):
        self.l = self.p[threading.get_ident()]
        Test_Item.Gemini_Test_Item.__init__(self, ip = self.G.telnet_ip, port = self.l['telnet_port'])
        

    def Gemini_BurnIn(self):
        """
        Gemini測試流程
        """
        self.Check_Telnet_Connect()
        #self.Boot_Up()
        self.Get_SN()
        #self.SFIS_Check_Route()
        #self.Set_Power()
        #self.Check_HW_SW_Ver()
        #self.Check_RTC()  
        #self.Check_HW_Monitor()
        #self.Check_Fan0_Speed()
        #self.Check_Fan100_Speed()
        #self.DRAM_Test()
        #self.SSD_Test()
        #self.Module_Signal_Check()
        #self.Set_Loopback_3_5W()
        #self.Traffic_Test()
        #self.Loopbak_Test() 
        #self.Rebbot()

    def Set_Power(self):
        run_times = self.l['run_times']
        if run_times % 3 == 1:
            self.Set_Two_Power()
        if run_times % 3 == 2:
            self.Set_A_Power()
        if run_times % 3 == 0:
            self.Set_B_Power()
    
    def Gemini_Reboot(self):
        self.Rebbot()
    



@Fail_Dealer()  
def Test_End_Function():
    Generate_Log.generate_log()
    online = Online_Flow()
    online.FTP_Upload()
    online.SFIS_Upload()
    online.IPLAS_Upload()



def Terminal_Flow():
    terminal = TerminalFlow()
    if not terminal.Check_ALL_Comport():
        return False
    if not terminal.Terminal_Server_Flow():
        return False
    return True
    

def Create_Debug_Log(l, logger_path):
    port = l['telnet_port']
    now_day = datetime.now().strftime("%m-%d")
    today_logger_path = fr"{logger_path}\{now_day}\{port}"

    l['dut_debug_logger'] = create_log.create_logger(today_logger_path, f"Gemini {port}_log")
    l['upload_debug_logger'] = create_log.create_logger(today_logger_path, f"Upload_{port}_log")
    l['sys_debug_logger'] = create_log.create_logger(today_logger_path, f"System_{port}_log")


def Gemini_Burn_In_Flow(telnet_port, device_ID):
    p = SingleTone_local()
    p.create_variable()
    l = p[threading.get_ident()]
    G = SingleTon_Global()

    l['device_id'] = device_ID
    l['telnet_port'] = telnet_port

    Create_Debug_Log(l, G.logger_path)
    
    condition = True
    while condition:
        Main_Flow = MainFlow()
        l['_test_start_time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        result = Main_Flow.Gemini_BurnIn()

        l['_test_end_time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        if result:

            """改變UI狀態，如果有error code，就顯示紅燈"""
            if len(l['_dut_error_code']):
                G.UI_Signal.single_status(l['telnet_port'], 'fail')

            """改變UI狀態，顯示紅燈"""
            if not Test_End_Function():#任何上傳失敗
                G.UI_Signal.single_status(l['telnet_port'], 'fail')
                
        
        else: #system exception
            """顯示紅燈，跳出提示視窗並結束測試"""    
            G.UI_Signal.single_status(l['telnet_port'], 'fail')
            G.UI_Signal.error_box('sys exception', l['_sys_error_msg'])
            p.init_variable()
            break

        p.init_variable()
        l['run_times'] += 1

        if l['run_times'] > G.total_run_times:
            G.UI_Signal.test_finish()
            condition = False
    

def Main_Test_Flow(**awags):
    G = SingleTon_Global()
    l = SingleTone_local()
    l.create_variable()
    get_veriable_from_controller(**awags)
    G.UI_Signal = UI_Contol(**awags)

    G.log_model = Log_Model.only_name
    G.main_debug_logger = create_log.create_logger(fr"{G.logger_path}\{datetime.now().strftime('%m-%d')}", f"Main_log")

    if not Terminal_Flow():
        """UI跳視窗並停止"""
        G.UI_Signal.error_box('termianl error', l['_sys_error_msg'])
        return 0
    
    #Gemini_Burn_In_Flow(2002, '992632')

    threads = list()
    for i, telent_port in enumerate(G.open_station):
        if telent_port:
            threads.append(threading.Thread(target = Gemini_Burn_In_Flow, args = (telent_port, G.sfis_deviceID_list[i],)))
            threads[i].start()
            time.sleep(0.5)
    ''' with ThreadPoolExecutor(max_workers=get_thread_num(G.open_station)) as executor:
        for i, telent_port in enumerate(G.open_station):
            if telent_port:
                futures = executor.submit(Gemini_Burn_In_Flow, telent_port, G.sfis_deviceID_list[i])
                time.sleep(1)
    
    for future in thread_list:
        if future.exception():
            print(future.exception())
            G.main_debug_logger.exception(f"exeption:{future.exception()}")  '''




def get_thread_num(open_station):
    i = 0
    for o in open_station:
        i = i+1 if o else i
    return i













if "__main__" == __name__:
    Main_Test_Flow()
    #Terminal_Flow(terminal_server_comport)
   
    #Gemini_Test_Flow(telnet_port)
    #Start_DUT_Initial()
    #Packaging_Loop()
    #Check_All_Comport()
    #DUT_Get_Counter_Thread() 