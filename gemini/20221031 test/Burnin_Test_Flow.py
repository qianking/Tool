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
from Global_Variable import SingleTon_Global, variable_setter, thread_local_set
from Log_Dealer import Log_Model
#import Generate_Log

local = threading.local()
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


class Fail_Dealer():

    def __init__(self):
        pass
        
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try: 
                func(*args, **kwargs)

            except Exception as ex:
                print(ex)
                """系統錯誤，基本上不應該出現，設定彈窗提示，並且停下來"""
                return False  

            else:
                return True
        return decorated


       
class TerminalFlow(Test_Item.Terminal_Server_Test_Item):

    G = SingleTon_Global()

    def __init__(self):
        self.l = local
        self.baud = '9600'
        Test_Item.Terminal_Server_Test_Item.__init__(self, self.l, port = self.G.terminal_comport, baud = self.baud)  
        

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
        self.Clear_Port_on_Terminal(2, 5)


class Online_Flow(Upload_FTP, SFIS_Function):
    
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



class MainFlow():

    G = SingleTon_Global()

    def __init__(self, device_ID, telnet_port):
        self.l = local
        print('in ain flow:', id(self.l))
        self.l.device_id = device_ID
        self.l.telnet_port = telnet_port
        now_day = datetime.now().strftime("%m-%d")
        today_logger_path = fr"{self.G.logger_path}\{now_day}\{telnet_port}"

        self.l.dut_debug_logger = create_log.create_logger(today_logger_path, f"Gemini {telnet_port}_log")
        self.test = Test_Item.Gemini_Test_Item(self.l, ip = self.G.telnet_ip, port = telnet_port)
 
    @Fail_Dealer()
    def Gemini_BurnIn(self):
        """
        Gemini測試流程
        """
        #self.Check_Telnet_Connect()
        #self.Boot_Up()
        result = self.test.Get_SN()
        print(local.upload_log)
        print(local.dut_info)
        if not result:
            return False
        
        
            
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
    

def Create_Debug_Log(logger_path):
    port = local.telnet_port
    now_day = datetime.now().strftime("%m-%d")
    today_logger_path = fr"{logger_path}\{now_day}\{port}"

    local.dut_debug_logger = create_log.create_logger(today_logger_path, f"Gemini {port}_log")
    local.upload_debug_logger = create_log.create_logger(today_logger_path, f"Upload_{port}_log")
    local.sys_debug_logger = create_log.create_logger(today_logger_path, f"System_{port}_log")


def Gemini_Burn_In_Flow(telnet_port, device_ID):
    G = SingleTon_Global()
    variable_setter(local)
    Create_Debug_Log(G.logger_path)
    
    condition = True
    while condition:
        Main_Flow = MainFlow(device_ID, telnet_port)
        
        result = Main_Flow.Gemini_BurnIn()

        if not result:
            print('end')

            """改變UI狀態，如果有error code，就顯示紅燈"""
            ''' if len(l.error_code):
                G.UI_Signal.single_status(l['telnet_port'], 'fail')
 '''
            """改變UI狀態，顯示紅燈"""
            ''' if not Test_End_Function():#任何上傳失敗
                G.UI_Signal.single_status(l['telnet_port'], 'fail') '''
                
        
        ''' else: #system exception
            """顯示紅燈，跳出提示視窗並結束測試"""    
            G.UI_Signal.single_status(l['telnet_port'], 'fail')
            G.UI_Signal.error_box('sys exception', l['_sys_error_msg'])
            p.init_variable()
            break '''

        local.run_time += 1

        if local.run_time > G.total_run_times:
            G.UI_Signal.test_finish()
            condition = False
    

def Main_Test_Flow(**awags):
    G = SingleTon_Global()
    variable_setter(local)
    get_veriable_from_controller(**awags)
    G.UI_Signal = UI_Contol(**awags)

    G.log_model = Log_Model.only_name
    G.main_debug_logger = create_log.create_logger(fr"{G.logger_path}", f"Main_log")

    if not Terminal_Flow():
        """UI跳視窗並停止"""
        G.UI_Signal.error_box('termianl error', l['_sys_error_msg'])
        return 0
    
    #Gemini_Burn_In_Flow(2002, '992632')

    thread_list = list()
    with ThreadPoolExecutor(max_workers=get_thread_num(G.open_station)) as executor:
        for i, telent_port in enumerate(G.open_station):
            if telent_port:
                futures = executor.submit(Gemini_Burn_In_Flow, telent_port, G.sfis_deviceID_list[i])
    
    for future in thread_list:
        if future.exception():
            print(future.exception())
            G.main_debug_logger.exception(f"exeption:{future.exception()}") 




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