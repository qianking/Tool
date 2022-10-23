import time
import os
import threading
from functools import wraps
import Burnin_Test_Item as Test_Item
import create_log as create_log
from concurrent.futures import ThreadPoolExecutor
from exceptions import Test_Fail, Upload_Fail
from Upload_Functions import Upload_FTP, SFIS_Function
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
                """測試錯誤，進入後續處理function"""
                return True  #設定為True代表會繼續下一輪的測試

            except Upload_Fail:
                print(self.Variable)
                """上傳錯誤，顯示到介面上? 後繼續? """
                return True

            except Exception:
                print(self.Variable.sys_error_msg)
                """系統錯誤，基本上不應該出現，設定彈窗提示，並且停下來"""
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

       
class TerminalFlow(Flow, Test_Item.Terminal_Server_Test_Item, metaclass = mChild):

    def __init__(self, terminal_comport):
        self.baud = '9600'
        self.Variable.open_log = True
        self.Variable.logger = create_log.create_logger(logger_path, 'main_log')
        super().__init__(port = terminal_comport, baud = self.baud)  

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
        self.Clear_Port_on_Terminal(2, 48)



class mChild(type(Flow), type(Test_Item.Gemini_Test_Item)):
    pass 

class MainFlow(Flow, Test_Item.Gemini_Test_Item, metaclass = mChild):

    def __init__(self, telnet_port, upload_flag):
        self.Variable.upload_flag = upload_flag
        self.Variable.open_log = True
        self.Variable.telnet_port = telnet_port
        self.Variable.logger = create_log.create_logger(logger_path, f"Gemini {telnet_port}_log")
        super().__init__(ip = telnet_ip, port = telnet_port, value_config_path = value_config_path) 

    def Gemini_BurnIn(self):
        """
        Gemini測試流程
        """
        self.Check_Telnet_Connect()
        self.Boot_Up()
        self.Set_Two_Power()
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

        test_log_path = r'.\log\test.txt'
        with open(test_log_path, 'w') as f:
            f.write(self.Variable.log)
        print(self.Variable.upload_log)


    def test_end_function(self, test_end = False):
        write_log
        if ftp_upload_funtion:
            Upload_FTP.ftb_upload_file

        if len(self.Variable.error_code):
            if not self.Variable.upload_flag:
                self.Variable.upload_flag = True
                self.upload_function()
        else:
            if not self.Variable.upload_flag and test_end:
                self.upload_function()
        
        return self.Variable.upload_flag
    
    def upload_function(self):
        if SFIS_upload_function:
            SFIS_Function.sfis_upload
        if iplas_upload_function:

            """IPLAS上傳"""

        """詢問是否需要上傳全部的細節或是只是要過站而已"""



def Gemini_Burn_In_Flow(telnet_port):
    run_times = 1
    upload_flag = False
    while run_times != 100:
        Main_Flow = MainFlow(telnet_port, upload_flag)
        if Main_Flow.Gemini_BurnIn():
            upload_flag = Main_Flow.test_end_function()
        else:
            break
        run_times += 1
        
    Main_Flow.test_end_function(test_end = True)
        
        



def Main_Test_Flow():

    comport = TerminalFlow(terminal_server_comport)
    comport.Check_ALL_Comport()
    comport.Clear_Port_on_Terminal()

    with ThreadPoolExecutor(max_workers=len(upload_file_list)) as executor:
        futures = executor.submit(Gemini_Burn_In_Flow, telnet_port)

    










if "__main__" == __name__:
    terminal_server_comport = 'COM7'
    telnet_port = 2002
    telnet_ip = "10.1.1.2"
    te = TerminalFlow(terminal_server_comport)
    #print(Terminal_Server.__dict__)
    te.Terminal_Server_Flow()
    #Gemini_Test_Flow(telnet_port)
    #Start_DUT_Initial()
    #Packaging_Loop()
    #Check_All_Comport()
    #DUT_Get_Counter_Thread() 