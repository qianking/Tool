import time
import os
import threading
from functools import wraps
from datetime import datetime
import Burnin_Test_Item as Test_Item
import create_log as create_log
from concurrent.futures import ThreadPoolExecutor
from exceptions import Test_Fail, Online_Fail
from Upload_Functions import Upload_FTP, SFIS_Function
from Global_Variable import SingleTon_Variable, SingleTon_Flag
from Log_Dealer import Log_Model
import Generate_Log


VERSION = ''

#telnet設定
telnet_ip = "10.1.1.2"
telnet_ports = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 
               2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

open_station = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sfis_deviceID = ['992632', '992631', '992630', '992629', '992628', '992627', '992626', '992625', '992624', '992622',
                '992632', '992631', '992630', '992629', '992628', '992627', '992626', '992625', '992624', '992622']


  
logger_path = r'.\debug'
value_config_path = r"D:\Qian\python\NPI\Gemini\value_config.ini"


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
SFIS_upload_function = True
sfis_op = ''
iplas_upload_function = True


#錯誤訊息
UI_msg = dict()


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
            for attr in local:
                value = local[attr]
                if callable(value) and attr != '__init__':
                    local[attr] = Fail_Dealer()(value)
        return super().__new__(cls, name, bases, local)


class Fail_Dealer():

    v = SingleTon_Variable()

    def __init__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                func(*args, **kwargs)

            except Test_Fail:
                """測試錯誤，進入後續處理function"""
                return True  #設定為True代表會繼續下一輪的測試，會先跑到test end function
            
            except Online_Fail:
                return False

            except Exception:
                print('sys_error_msg:', self.v.sys_error_msg)
                """系統錯誤，基本上不應該出現，設定彈窗提示，並且停下來"""
                return False  

            else:
                print(self.v.log)
                print('upload_log:', self.v.upload_log)
                return True
        return decorated


class Flow(metaclass = Flow_MetaClass):
    pass
       
class TerminalFlow(Test_Item.Terminal_Server_Test_Item):

    v = SingleTon_Variable()

    def __init__(self):
        self.v.open_log = True
        self.baud = '9600'
        Test_Item.Terminal_Server_Test_Item.__init__(self, port = self.v.terminal_comport, baud = self.baud)  
        

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
    
    v = SingleTon_Variable()
    f = SingleTon_Flag()

    def __init__(self, runtimes = 0):
        self.runtims = runtimes
        Upload_FTP.__init__(self, self.v.ftp_upload_path, self.v)
        SFIS_Function.__init__(self, self.v)

    def FTP_Upload(self):
        self.ftb_upload_file()

    def SFIS_Check_Route(self):
        if self.f.upload_func_open:
            if not self.v.been_checkroute:
                self.sfis_checkroute(self.v.dut_info['SN'])
                self.v.been_checkroute = True
    
    def SFIS_Upload(self):
        if self.f.upload_func_open:
            if not self.v.been_sfis_upload and (len(self.v.error_code) or self.v.run_times == self.v.total_run_times): #如果有ERROR CODE並且還沒上傳過
                self.v.been_sfis_upload = True
                self.sfis_upload(self.v.dut_info['SN'], self.v.error_code, self.v.sfis_log)
        
    def IPLAS_Upload(self):
        if self.f.upload_func_open:
            if not self.v.check_route_fail:
                pass

    def test(self):
        for i in range(6):
            print(i)
            if i == 5:
                raise Exception

class mChild(type(Flow), type(Test_Item.Gemini_Test_Item)):
    pass 

class MainFlow(Flow, Test_Item.Gemini_Test_Item, Online_Flow, metaclass = mChild):

    v = SingleTon_Variable()

    def __init__(self):
        Test_Item.Gemini_Test_Item.__init__(self, ip = telnet_ip, port = self.v.telnet_port, value_config_path = value_config_path) 

    def Gemini_BurnIn(self):
        """
        Gemini測試流程
        """
        self.Check_Telnet_Connect()
        self.Boot_Up()
        self.Get_SN()
        self.SFIS_Check_Route()

        ''' self.Set_Two_Power()
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
        self.Loopbak_Test() '''
        self.Rebbot()

        ''' test_log_path = r'.\test.txt'
        with open(test_log_path, 'w+', newline='', encoding="utf-8") as f:
            f.write(self.v.log) '''
    
    def Gemini_Reboot(self):
        self.Rebbot()
    



@Fail_Dealer()  
def Test_End_Function(run_times):
    '''write_log'''
    online = Online_Flow(run_times)
    online.FTP_Upload()
    online.SFIS_Upload()
    online.IPLAS_Upload()


@Fail_Dealer()
def Terminal_Flow():
    ter = SingleTon_Variable()
    terminal = TerminalFlow()
    terminal.Check_ALL_Comport()
    terminal.Terminal_Server_Flow()
    

def Create_Debug_Log():
    V = SingleTon_Variable()
    V.main_debug_logger = create_log.create_logger(logger_path, f"Main_log")
    V.dut_debug_logger = create_log.create_logger(logger_path, f"Gemini {V.telnet_port}_log")
    V.sfis_debug_logger = create_log.create_logger(logger_path, f"SFIS_{V.telnet_port}_log")
    V.ftp_debug_logger = create_log.create_logger(logger_path, f"FTP_{V.telnet_port}_log")
    V.iplas_debug_logger = create_log.create_logger(logger_path, f"IPLAS_{V.telnet_port}_log")


def Gemini_Burn_In_Flow(telnet_port, device_ID):
    Create_Debug_Log()
    condition = True
    Main_f = SingleTon_Flag()
    Main_v = SingleTon_Variable()
    
    Main_v.log_model = Log_Model.only_name
    Main_v.device_id = device_ID
    Main_v.telnet_port = telnet_port

    Main_v.run_times = 1

    while condition:
        Main_Flow = MainFlow()
        Main_v.test_start_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        result = Main_Flow.Gemini_BurnIn()
        
        Main_v.test_end_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        if result:
            if len(Main_v._dut_error_code):
                
                """改變UI狀態，如果有error code，就顯示紅燈"""
            if not Test_End_Function():#任何上傳失敗
                """改變UI狀態，顯示紅燈"""
            
        else:
            """顯示紅燈，跳出提示視窗並結束測試"""
            Main_v.clear_all()
            break

        Main_v.clear_all()
        Main_v.run_times += 1

        if Main_v.run_times > Main_v.total_run_times:
            condition = False
    

def Main_Test_Flow():
    Main_V = SingleTon_Variable()
    Main_F = SingleTon_Flag()

    """去拿UI給的變數存到Main_V, Main_F中
    Main_V.Variable.op = 'LA2100645'
    """
    if not Terminal_Flow():
        """UI跳視窗，全部紅色並停止"""
        return 0

    Main_V.clear_all()
    
    with ThreadPoolExecutor(max_workers=len(upload_file_list)) as executor:
        futures = executor.submit(Gemini_Burn_In_Flow, telnet_port, device_ID)
















def test():
    Main_Flow = MainFlow()
    Main_Flow.Gemini_BurnIn()


def test_main(telnet_port, terminal_comport):
    Main_V = SingleTon_Variable()
    Main_F = SingleTon_Flag()
    Main_V.telnet_port = telnet_port
    Main_V.terminal_comport = terminal_comport
    Create_Debug_Log()
    Terminal_Flow()
    Main_V.clear_all()
    test()
    #print('SN:', Main_V.dut_info['SN'])









if "__main__" == __name__:
    terminal_server_comport = 'COM7'
    telnet_port = 2002
    telnet_ip = "10.1.1.2"
    #Terminal_Flow(terminal_server_comport)
    test_main(telnet_port, terminal_server_comport)
    #Gemini_Test_Flow(telnet_port)
    #Start_DUT_Initial()
    #Packaging_Loop()
    #Check_All_Comport()
    #DUT_Get_Counter_Thread() 