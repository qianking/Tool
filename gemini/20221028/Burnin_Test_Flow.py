import time
import os
from copy import deepcopy
import threading
from datetime import datetime
from tkinter import Variable
import Burnin_log as Write_log
from functools import wraps
import Burnin_Test_Item as Test_Item
import file_util
import FTP
import create_log
from concurrent.futures import ThreadPoolExecutor
from Upload_Functions import Upload_FTP, SFIS_Function
from exceptions import Test_Fail
from Log_Dealer import Log_Model
import Generate_Log
from Global_Variable import SingleTon_Global,Thread_Global

VERSION = ''

#telnet設定
telnet_ip = "10.1.1.2"
telnet_ports = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 
               2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
open_station = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sfis_deviceID = {2002:'992632', 2003:'992631', 2004:'992630', 2005:'992629', 2006:'992628', 2007:'992627', 2008:'992626', 2009:'992625', 2010:'992624', 2011:'992622',
                2012:'992632', 2013:'992631', 2014:'992630', 2015:'992629', 2016:'992628', 2017:'992627', 2018:'992626', 2019:'992625', 2020:'992624', 2021:'992622'}
    
#logger設定
logger_path = r'.\debug'
test_log_path = r'.\log\test.txt'

value_config_path = r"D:\Qian\python\NPI\Gemini\value_config.ini"

SFIS_logger = file_util.create_logger(logger_path, 'SFIS_log')


#測試參數
signal = None
serial_name = 'EZ1K_A1'
serial_port = '8'
terminal_server_comport = 'COM4'
pg_comport = 'COM5'
package_machine = 'Nustream'
test_time = 48
ftp_upload_funtion = False
ftp_upload_path = '/SWITCH/EZ1K-ORT'
SFIS_function = True
sfis_op = ''

#封包機參數
nustream_initial_tcl_path = r'C:\TCL\bin\DUT1_1000M_10s_card.tcl'
nustream_packaging_tcl_path = r'C:\TCL\bin\DUT1_1000M_480s_card.tcl'   
pg_initial_test_time = 20          #pg在initial裡面的測試時間(s)
pg_packing_test_time = 470         #pg在打封包測試裡面的測試時間(s)
packing_rest_time = 116             #116

#錯誤訊息
UI_msg = dict()


sfis_log_other = str()
dut_SSN_dic = dict()
all_sfis_log = dict()
all_sfis_error_code = dict()
checkroute_data = dict()



#測試完儲存下來的DUT資訊(port : serial name)，會先送到controller，等到打封包測試時再送回來
dut_finish_initial_data = dict()


#region 接入從controller下達的參數
def get_veriable_from_controller(**kwargs):
    global signal

    global VERSION
    global open_station
    global serial_name
    global serial_port
    global terminal_server_comport
    global pg_comport
    global package_machine
    global test_time
    global ftp_upload_funtion
    global ftp_upload_path
    global SFIS_function
    global sfis_op

    global dut_finish_initial_data

    signal = kwargs.get('signal')
    config = kwargs.get('config')
    VERSION = kwargs.get('VERSION')
    if config:
        serial_name = config['serial_name']
        serial_port = str(config['serial_port'])
        terminal_server_comport = config['terminal_server_comport']
        pg_comport = config['pg_comport']
        package_machine = config['package_machine']
        test_time = config['test_time']
        open_station = config['open_station']
        ftp_upload_funtion = config['ftp_upload_funtion']
        ftp_upload_path = config['ftp_upload_path']
        ftp_upload_path = ftp_upload_path.replace('\\', '/').strip('/')
        SFIS_function = config['SFIS_function']
        sfis_op = config['op']
        
    if kwargs.get('dut_data'):
        dut_finish_initial_data = kwargs['dut_data']
    
#endregion

#region 送訊息到UI
def send_to_ui(msg):
    """
    送訊息到UI controller
    """
    if signal:   
        signal.status.emit(msg)
#endregion

class Flow_MetaClass(type):
    def __new__(cls, name, bases, local):
        if len(bases):
            for base in bases:
                if base != Flow:
                    Variable = base.Variable
            local['Variable'] = Variable
            for attr in local:
                value = local[attr]
                if callable(value) and attr != '__init__':
                    local[attr] = Fail_Dealer(Variable)(value)
        return super().__new__(cls, name, bases, local)

class Fail_Dealer():
    def __init__(self, Variable):
        self.Variable = Variable

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                func(*args, **kwargs)

            except Test_Fail:
                print(self.Variable)
                return True
                
            except Exception as ex:
                print(ex)
                print(self.Variable.sys_error_msg)
                return False

            else:
                print(self.Variable.log)
                print(self.Variable.upload_log)
                return True
        return decorated



class Flow(metaclass = Flow_MetaClass):
    pass

class mChild(type(Flow), type(Test_Item.Terminal_Server_Test_Item)):
    pass
       
class Terminal_Server(Flow, Test_Item.Terminal_Server_Test_Item, metaclass = mChild):

    v = SingleTon_Global()

    def __init__(self):
        self.baud = '9600'
        self.logger = file_util.create_logger(logger_path, 'main_log')
        super().__init__(port = self.v.terminal_server_comport, baud = self.baud, logger = self.logger)  

    def Check_All_Comport(self):
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
    
    f = SingleTon_Global()

    def __init__(self, threal_local, thread_global):
        self.threal_local = threal_local
        self.thread_global = thread_global
        Upload_FTP.__init__(self, self.f.ftp_upload_path, threal_local, thread_global, self.f.ftp_debug_logger)
        SFIS_Function.__init__(self, threal_local, thread_global ,self.f, self.f.sfis_debug_logger)

    def FTP_Upload(self):
        self.ftb_upload_file(self.threal_local.ftp_local_path, self.threal_local.ftp_remote_path)

    def SFIS_Check_Route(self):
        if self.f.upload_func_open:
            if not self.thread_global.been_checkroute:
                self.sfis_checkroute(self.threal_local.dut_info['SN'])
                self.thread_global.been_checkroute = True

        return self.thread_global
    
    def SFIS_Upload(self):
        if self.f.upload_func_open:
            if not self.thread_global.been_sfis_upload and (len(self.threal_local.error_code) or self.thread_global.run_times == self.f.total_run_times): #如果有ERROR CODE並且還沒上傳過
                self.thread_global.been_sfis_upload = True
                self.sfis_upload(self.v.dut_info['SN'], self.v.error_code, self.v.sfis_log)


    def IPLAS_Upload(self):
        if self.f.upload_func_open:
            if not self.v.check_route_fail:
                pass

class mChild(type(Flow), type(Test_Item.Gemini_Test_Item)):
    pass 

class Gemini(Flow, Test_Item.Gemini_Test_Item, metaclass = mChild):

    f = SingleTon_Global()

    def __init__(self, telnet_port, thread_global):
        self.thread_global = thread_global
        self.telnet_port = telnet_port
        self.Gemini_logger = file_util.create_logger(logger_path, f"Gemini {telnet_port}_log")
        super().__init__(ip = self.f.telnet_ip, port = self.telnet_port, logger = self.Gemini_logger, value_config_path = self.f.value_config_path)  

    def Gemini_Test_Flow(self):
        """
        Gemini測試流程
        """
        self.Gemini_logger.debug(f"port [{self.telnet_port}] in [Gemini_Test_Flow]")
        self.Check_Telnet_Connect()
        self.Boot_Up()
        #self.Set_Two_Power()
        #self.Get_SN()
        self.online = Online_Flow(self.thread_global, self.Variable)
        self.thread_global = self.online.SFIS_Check_Route()

        self.Check_HW_SW_Ver()
        self.Check_RTC()    
        self.Check_HW_Monitor()
        self.Check_Fan0_Speed()
        self.Check_Fan100_Speed()
        self.DRAM_Test()
        self.SSD_Test()
        self.Module_Signal_Check()
        self.Set_Loopback_3_5W()
        self.Traffic_Test()
        self.Loopbak_Test()

        with open(test_log_path, 'w') as f:
            f.write(self.Variable.log)
        print(self.Variable.upload_log)




        
def Terminal_Flow():
    te = Terminal_Server()
    if not te.Check_All_Comport():
        return False
    if not te.Terminal_Server_Flow():
        return False
    return True


def Test_End_Function(threal_local, thread_global):
    threal_local, thread_global = Generate_Log.generate_log(threal_local, thread_global)
    online = Online_Flow(threal_local, thread_global)
    online.FTP_Upload()
    online.SFIS_Upload()
    online.IPLAS_Upload()

def Create_Debug_Log():
    V = SingleTon_Global()
    V.sfis_debug_logger = create_log.create_logger(logger_path, f"SFIS_log")
    V.ftp_debug_logger = create_log.create_logger(logger_path, f"FTP_log")
    V.iplas_debug_logger = create_log.create_logger(logger_path, f"IPLAS_log")

def Main():
    Main_F = SingleTon_Global()

    if not Terminal_Flow():
        """跳出提示視窗"""
        return 0

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = executor.submit(Gemini_Burn_In_Flow, 2002, 'device_ID')

def Gemini_Burn_In_Flow(telnet_port, device_ID):
    Main_F = SingleTon_Global()
    condition = True
    thread_global = Thread_Global()
    Main_F.log_model = Log_Model.only_name
    thread_global.device_id = device_ID
    thread_global.telnet_port = telnet_port
    thread_global.run_times = 1
    while condition:
        thread_global.test_start_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        gemini = Gemini(telnet_port, thread_global)
        result = gemini.Gemini_Test_Flow()
        threal_local = gemini.Variable
        thread_global = gemini.thread_global
        thread_global.test_end_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        if result:
            if len(threal_local.error_code):
                thread_global.dut_been_test_fail = True
                """改變UI狀態，如果有error code，就顯示紅燈"""
            if not Test_End_Function(threal_local, thread_global):#任何上傳失敗
                """改變UI狀態，顯示紅燈"""
        else:
            """顯示紅燈，跳出提示視窗並結束測試"""
            break
        
        thread_global.run_times += 1
        if thread_global.run_times > Main_F.total_run_times:
            condition = False

if "__main__" == __name__:
    #print(Terminal_Server.__dict__)
    Main()
    #Gemini_Test_Flow(telnet_port)
    #Start_DUT_Initial()
    #Packaging_Loop()
    #Check_All_Comport()
    #DUT_Get_Counter_Thread() 