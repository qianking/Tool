import time
import os
import threading
from functools import wraps
from datetime import datetime
import Burnin_Test_Item as Test_Item
from datetime import datetime
import create_log as create_log
from concurrent.futures import ThreadPoolExecutor
from exceptions import Test_Fail, Online_Fail, CheckRoute_Fail
from Upload_Functions import Upload_FTP, SFIS_Function
from Global_Variable import SingleTon_Global, variable_setter, thread_local_set

import Generate_Log
import exceptions
from iPLAS.py_producer import PyProducer

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
        G.ftp_function = config['ftp_function']
        G.ftp_upload_path = config['ftp_upload_path']
        G.op = config['op']
        if G.test_time == 0:
            G.total_run_times = 1
        else:
            G.total_run_times = G.test_time*6
#endregion


#region 送訊息到UI
class UI_Contol():

    def __init__(self, **awags):
        self.signal = awags.get('signal')
    
    def init_finish(self):
        """
        初始化完成
        """
        ui_lock.acquire()
        if self.signal: 
            self.signal.init_finish.emit()
        ui_lock.release()

    def back_to_origin(self):
        """
        回到原始設定
        """
        ui_lock.acquire()
        if self.signal: 
            self.signal.back_to_origin.emit()
        ui_lock.release()   

    def single_status(self, telnet_port, status, color = None):
        """
        改變單一station的狀態
        status: ['fail', 'done']
        color: ['red', 'lightgreen']
        """

        ui_lock.acquire()
        if self.signal: 
            self.signal.single_light.emit((telnet_port, status, color))
        ui_lock.release()

    def all_status(self, color, txt):
        """
        改變全部station的狀態
        color: ['lightgreen', 'red']
        """
        ui_lock.acquire()
        if self.signal: 
            self.signal.all_light.emit((color, txt))
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

            except Test_Fail:
                return False

            except Online_Fail:
                return False
            
            except CheckRoute_Fail:
                return 'CheckRoute_Fail'

            except Exception as ex:
                print(ex)
                """系統錯誤，基本上不應該出現，設定彈窗提示，並且停下來"""
                return 'Exception' 

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
        self.Clear_Port_on_Terminal(self.G.open_station)
          
       


class Online_Flow(Upload_FTP, SFIS_Function):
    
    G = SingleTon_Global()

    def __init__(self):
        self.l = local

        Upload_FTP.__init__(self, self.G.ftp_upload_path, self.l)
        SFIS_Function.__init__(self, self.G.op, self.l)

        self.l.upload_debug_logger.debug(f"{self.l.run_times:-^50}")

    def FTP_Upload(self):
        if self.G.ftp_function:
            self.ftb_upload_file(self.l.ftp_local_path, self.l.ftp_remote_path)

    def SFIS_Check_Route(self):
        if self.G.online_function:
            if not self.l.been_checkroute:
                self.sfis_checkroute(self.l.dut_info['SN'])
                self.l.been_checkroute = True
      
    def SFIS_Upload(self):
        if self.G.online_function:
            if not self.l.been_sfis_upload and (len(self.l.error_code) or self.l.run_times == self.G.total_run_times): #如果有ERROR CODE並且還沒上傳過
                if self.l.dut_info.get('SN'):
                    self.l.been_sfis_upload = True
                    self.sfis_upload(self.l.dut_info['SN'], self.l.error_code, self.l.sfis_log)
    

    def SFIS_Get_SN(self):
        if self.G.online_function:
            if not self.l.been_sfis_upload and (len(self.l.error_code) or self.l.run_times == self.G.total_run_times):
                if self.l.dut_info.get('SN'):
                    self.sfis_get_dut_sn(self.l.dut_info.get('SN'))
                else:
                    self.l.sfis_get_sn_fail = True

    def IPLAS_Upload(self):
        if self.G.online_function:
            if not self.l.been_sfis_upload and (len(self.l.error_code) or self.l.run_times == self.G.total_run_times):
                if not self.l.check_route_fail and not self.l.sfis_get_sn_fail:
                    PyProducer.send_ts_data(local.iplas_log_path, local.iplas_log)



class MainFlow():

    G = SingleTon_Global()

    def __init__(self):
        self.l = local
        self.test = Test_Item.Gemini_Test_Item(self.l, ip = self.G.telnet_ip, port = self.l.telnet_port)
        self.online = Online_Flow()
 
    @Fail_Dealer()
    def Gemini_BurnIn(self):
        """
        Gemini測試流程
        """
        self.test.Check_Telnet_Connect()
        if self.l.run_times != 1:
            self.test.Reboot()
        self.test.Boot_Up()
        self.test.Get_SN()
        self.online.SFIS_Check_Route()
        self.Set_Power()
        self.test.Check_HW_SW_Ver()
        self.test.Check_RTC()  
        self.test.Check_HW_Monitor()
        self.test.Check_Fan0_Speed()
        self.test.Check_Fan100_Speed()
        self.test.Fan_auto_mode()
        self.test.DRAM_Test()
        self.test.SSD_Test()
        self.test.Module_Signal_Check()
        self.test.Set_Loopback_3_5W()
        self.test.Traffic_Test()
        self.test.Loopbak_Test()

        if local.run_times == self.G.total_run_times:
            if not local.dut_been_test_fail:
                self.test.Set_Green_light()
            else:
                self.test.Set_Red_light()
        
        

    def Set_Power(self):
        if self.l.run_times % 3 == 1:
            self.test.Set_Two_Power()

        if self.l.run_times % 3 == 2:
            self.test.Set_A_Power()

        if self.l.run_times % 3 == 0:
            self.test.Set_B_Power()



@Fail_Dealer()
def Test_End_Function():
    online = Online_Flow()
    online.SFIS_Get_SN()
    Generate_log_and_Upload()
    online.SFIS_Upload()
    online.IPLAS_Upload()


def Generate_log_and_Upload():
    G = SingleTon_Global()
    Generate_Log.generate_log(local, G)
    online = Online_Flow()
    online.FTP_Upload()


@Fail_Dealer()
def Terminal_Flow():
    terminal = TerminalFlow()
    terminal.Check_ALL_Comport()  
    terminal.Terminal_Server_Flow()
  

def create_main_logger():
    G = SingleTon_Global()
    now_day = datetime.now().strftime("%m-%d")
    main_log_path = fr"{G.logger_path}\{now_day}"
    os.makedirs(main_log_path, exist_ok = True)
    G.main_debug_logger = create_log.create_logger(main_log_path, 'Main_log')

def Create_Debug_Log(logger_path):
    port = local.telnet_port
    now_day = datetime.now().strftime("%m-%d")
    now_time = datetime.now().strftime("%H-%M-%S")
    today_logger_path = fr"{logger_path}\{now_day}\{port}"
    os.makedirs(today_logger_path, exist_ok = True)
    local.dut_debug_logger = create_log.create_logger(today_logger_path, f"Gemini_{port}_log")
    local.upload_debug_logger = create_log.create_logger(today_logger_path, f"Upload_{port}_log")
    local.sys_debug_logger = create_log.create_logger(today_logger_path, f"System_{port}_log")




def Gemini_Burn_In_Flow(telnet_port, device_ID):
    G = SingleTon_Global()
    variable_setter(local)
    local.telnet_port = telnet_port
    local.device_id = device_ID
    Create_Debug_Log(G.logger_path)
    
    condition = True
    while condition:

        G.UI_Signal.single_status(local.telnet_port, f'cycle {local.run_times}')

        Main_Flow = MainFlow()

        local.test_start_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        result = Main_Flow.Gemini_BurnIn()

        local.test_end_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(local.upload_log)

        if result == True or result == False: #true為pass，false為有failed

            if len(local.error_code):  #如果有error code
                G.UI_Signal.single_status(local.telnet_port, 'fail', 'red')

        
            result = Test_End_Function() #進去online function
            if result == False: #任何online function失敗
                Generate_log_and_Upload() #更新log、上傳FTP
                G.UI_Signal.single_status(local.telnet_port, 'fail', 'red')
                
            if result == 'Exception':
                G.UI_Signal.single_status(local.telnet_port, 'exception', 'red')
                if len(local.sys_error_msg):
                    msg = "\n".join(local.sys_error_msg)
                    print('exception:', msg)
                    local.sys_debug_logger.exception(f'Exception: {msg}')
                    G.UI_Signal.error_box('sys exception', msg)
                    G.UI_Signal.back_to_origin()
                    break

        elif result == 'CheckRoute_Fail':
            G.UI_Signal.single_status(local.telnet_port, 'check route fail', 'red')
            Generate_log_and_Upload()
            break
        
        elif result == 'Exception':  
            G.UI_Signal.single_status(local.telnet_port, 'exception', 'red')
            if len(local.sys_error_msg):
                msg = "\n".join(local.sys_error_msg)
                print('exception:', msg)
                local.sys_debug_logger.exception(f'Exception: {msg}')
                G.UI_Signal.error_box('sys exception', msg)
                G.UI_Signal.back_to_origin()
            break 
        
        time.sleep(60)

        local.run_times += 1
        thread_local_set(local)
        
        if local.run_times > G.total_run_times:
            G.UI_Signal.test_finish()
            if local.dut_been_test_fail:
                G.UI_Signal.single_status(local.telnet_port, 'Done')
            else:
                G.UI_Signal.single_status(local.telnet_port, 'PASS')

            condition = False
        
        




def Clear_Port_Flow(**awags):
    G = SingleTon_Global()
    variable_setter(local)
    get_veriable_from_controller(**awags)
    G.UI_Signal = UI_Contol(**awags)
    create_main_logger()

    G.UI_Signal.all_status('lightgreen', 'clear port')

    result = Terminal_Flow()
    if result == False or result == 'Exception':
        """UI跳視窗並停止"""
        msg = "\n".join(local.sys_error_msg)
        G.main_debug_logger.debug(f'Exception:{msg}')
        G.UI_Signal.error_box('termianl error', msg)
        G.UI_Signal.back_to_origin()
        return 0

    G.UI_Signal.all_status('lightgreen', 'done')
    G.UI_Signal.init_finish()

    
def Main_Test_Flow(**awags):
    G = SingleTon_Global()
    get_veriable_from_controller(**awags)
    G.UI_Signal = UI_Contol(**awags)
    
    
    thread_list = list()
    with ThreadPoolExecutor(max_workers=get_thread_num(G.open_station)) as executor:
        for i, telent_port in enumerate(G.open_station):
            if telent_port:
                futures = executor.submit(Gemini_Burn_In_Flow, telent_port, G.sfis_deviceID_list[i])
    
    for future in thread_list:
        if future.exception():
            print(future.exception())
            G.main_debug_logger.exception(f"exeption:{future.exception()}") 
            G.UI_Signal.error_box('sys exception', future.exception())
            G.UI_Signal.back_to_origin()


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