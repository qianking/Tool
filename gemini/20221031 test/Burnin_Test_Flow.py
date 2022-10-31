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
import Generate_Log
import exceptions

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

            except Online_Fail:
                return False

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


    @Fail_Dealer()
    def Check_ALL_Comport(self):
        """
        確認terminal server和pg的port口是否正常
        """
        if not self.Check_Comport():
            return True
        return True


    @Fail_Dealer()
    def Terminal_Server_Flow(self):
        """
        terminal server清線
        """
        if not self.Enter_en_Mode():
            return True
        if not self.Clear_Port_on_Terminal(2, 5):
            return True
        return True


class Online_Flow(Upload_FTP, SFIS_Function):
    
    G = SingleTon_Global()

    def __init__(self, l):
        self.l = l

        Upload_FTP.__init__(self, self.G.ftp_upload_path, self.l)
        SFIS_Function.__init__(self, self.G.op, self.l)

        self.l.upload_debug_logger.debug(f"{self.l.run_times:-^50}")


    @Fail_Dealer()
    def FTP_Upload(self):
        self.ftb_upload_file(self.l.ftp_local_path, self.l.ftp_remote_path)


    @Fail_Dealer()
    def SFIS_Check_Route(self):
        if self.G.online_function:
            if not self.l['been_checkroute']:
                self.sfis_checkroute(self.l.dut_info['SN'])
                self.l['been_checkroute'] = True

    @Fail_Dealer()
    def SFIS_Get_SN(self):
        if self.G.online_function:
            pass

    @Fail_Dealer()        
    def SFIS_Upload(self):
        if self.G.online_function:
            if not self.l['been_sfis_upload'] and (len(self.l.dut_error_code) or self.l.run_times == self.G.total_run_times): #如果有ERROR CODE並且還沒上傳過
                self.l['been_sfis_upload'] = True
                self.sfis_upload(self.l.dut_info['SN'], self.l.dut_error_code, self.l.sfis_log)
    
    
    @Fail_Dealer()    
    def IPLAS_Upload(self):
        if self.G.online_function:
            if not self.l.check_route_fail:
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
        self.online = Online_Flow(self.l)
 
    @Fail_Dealer()
    def Gemini_BurnIn(self):
        """
        Gemini測試流程
        """
        result = self.test.Check_Telnet_Connect()
        if not result:
            return True

        result = self.test.Boot_Up()
        if not result:
            return True

        result = self.test.Get_SN()
        if not result:
            return True
          
        result = self.online.SFIS_Check_Route()
        if not result:
            return True

        result = self.Set_Power()
        if not result:
            return True

        result = self.test.Check_HW_SW_Ver()
        if not result:
            return True

        result = self.test.Check_RTC()  
        if not result:
            return True

        result = self.test.Check_HW_Monitor()
        if not result:
            return True

        result = self.test.Check_Fan0_Speed()
        if not result:
            return True

        result = self.test.Check_Fan100_Speed()
        if not result:
            return True

        result = self.test.DRAM_Test()
        if not result:
            return True

        result = self.test.SSD_Test()
        if not result:
            return True

        result = self.test.Module_Signal_Check()
        if not result:
            return True

        result = self.test.Set_Loopback_3_5W()
        if not result:
            return True

        result = self.test.Traffic_Test()
        if not result:
            return True

        result = self.test.Loopbak_Test()
        if not result:
            return True

        result = self.test.Rebbot()
        if not result:
            return True
        
        return True


    def Set_Power(self):
        run_times = self.l.run_times
        if run_times % 3 == 1:
            result = self.test.Set_Two_Power()
            if not result:
                return False

        if run_times % 3 == 2:
            result = self.test.Set_A_Power()
            if not result:
                return False

        if run_times % 3 == 0:
            result = self.test.Set_B_Power()
            if not result:
                return False
    
    def Gemini_Reboot(self):
        result = self.test.Rebbot()
        if not result:
            return False
    


 
def Test_End_Function():
    try:
        Generate_Log.generate_log(local)
    except Exception as ex:
        error_msg = exceptions.error_dealer(ex)
        local.sys_error_msg.append(error_msg)
        return False
        
    online = Online_Flow(local)
    if not online.FTP_Upload():
        return False
    if not online.SFIS_Upload():
        return False
    if not online.IPLAS_Upload():
        return False
    return True



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

        local.test_start_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        result = Main_Flow.Gemini_BurnIn()

        local.test_end_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        if result:

            """改變UI狀態，如果有error code，就顯示紅燈"""
            if len(local.error_code):
                G.UI_Signal.single_status(local.telnet_port, 'fail')

            """改變UI狀態，顯示紅燈"""
            if not Test_End_Function():#任何上傳失敗
                G.UI_Signal.single_status(local.telnet_port, 'fail')
                if len(local.sys_error_msg):
                    msg = ",".join(local.sys_error_msg)
                    G.UI_Signal.error_box('sys exception', msg)
        

        else: #system exception
            """顯示紅燈，跳出提示視窗並結束測試"""    
            G.UI_Signal.single_status(local.telnet_port, 'fail')
            if len(local.sys_error_msg):
                msg = ",".join(local.sys_error_msg)
                G.UI_Signal.error_box('sys exception', msg)
            thread_local_set(local)
            break 

        local.run_time += 1
        thread_local_set(local)
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
        msg = ".".join(local.sys_error_msg)
        G.UI_Signal.error_box('termianl error', msg)
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