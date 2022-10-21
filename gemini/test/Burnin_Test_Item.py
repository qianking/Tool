from tabnanny import check
from textwrap import wrap
import time
import datetime
from functools import wraps
from copy import deepcopy
from comport_and_telnet import Telnet
from comport_and_telnet import COM
import Global_Variable 
import Test_item_check
import error_code
from exceptions import TimeOutError, TestItemFail, Test_Fail

Variable = None

class myMetaClass(type):
    def __new__(cls, name, bases, local):
        print(bases)
        print(local)
        for attr in local:
            value = local[attr]
            if callable(value) and attr != '__init__':
                local[attr] = log_deco()(value)
        
        return super().__new__(cls, name, bases, local)
    
class log_deco():
    def __init__(self):
        pass
    
    def get_runtime(self):
        runtime = str(time.time() - self.start_time)
        runtime = int(runtime.split('.')[0])
        return runtime

       
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            ''' func(*args, **kwargs)
            return True  '''
            try:
                self.start_time = time.time()
                test_item = func.__name__
                print(test_item)
                self.Variable.logger.debug(f'terminal server in [{test_item}]')
                func(*args, **kwargs)

            #當telnet或是 comport timeout時會進到這裡
            except TimeOutError:
                Variable.logger.debug(f'terminal server failed in [{test_item}]')
                self.error_function(test_item)
                raise Test_Fail
                
            
            #測試項目失敗會進到這裡
            except TestItemFail as test_item_data:
                Variable.logger.debug(f'terminal server failed in [{test_item}]')
                self.error_function(test_item, test_item_data.args[0])
                raise Test_Fail
               

            #當發生系統性的錯誤時會進到這裡
            except Exception as ex:
                print(ex)
                Variable.logger.debug(f'terminal server failed in [{test_item}]')
                self.sys_exception(ex)
                raise Exception
            
            else:
                Variable.upload_log = (test_item, (1, 'PASS', None, None, None, None, self.get_runtime()))
        
        return decorated 

    def error_function(self, test_item, test_item_data = None):
        if test_item_data[0]:
            test_item = test_item_data[0]

        #error = error_code[test_item_data[0]]  #get error code
        error = 'A12345'

        Variable.upload_log = (test_item, (0, 'FAIL', test_item_data[1][0], test_item_data[1][1], test_item_data[1][2], error, self.get_runtime()))

        Variable.test_error_msg = test_item_data[2]

    def sys_exception(self, ex):
            
        #只有這三種錯誤式系統的exception，所以直接在UI彈出提示視窗   
        if 'FileNotFoundError' in str(ex):           #console連接錯誤 電腦找不到這個port口
            #print('Comport 找不到指定port口')
            Variable.sys_error_msg = 'Comport 找不到指定port口'
                
        elif 'PermissionError' in str(ex):             #console連接錯誤 port口被其他程式使用
            #print('Comport Port口被占据')
            Variable.sys_error_msg = 'Comport Port口被占据'
        
        elif 'WinError 10061' in str(ex):                    #telnet連接錯誤 telnet被占線
            #print('Telnet连线被占据')
            Variable.sys_error_msg = 'Telnet连线被占据'

        else:
            Variable.sys_error_msg = str(ex)

          
class Terminal_Server_Test_Item(metaclass = myMetaClass):

    def __init__(self, **args):
        global Variable
        Variable = args['Variable']
        self.connect = COM(args['port'], args['baud'], Variable)
        self.check_test = Test_item_check.Terminal_Test()


    def Check_Comport(self):
        """
        開啟並確認是否能連上Terminal server
        """
        self.connect.check_connect()
        

    def Enter_en_Mode(self):
        """
        進入Router#，如果有密碼就打密碼:pega123
        """
        self.connect.send_and_receive('', 'Router', 5, 'Password:')
        if self.check_test.If_PassWord(Variable.tmp_log):
            self.connect.send_and_receive('pega123', 'Router>', 5)            
        self.connect.send_and_receive('en', 'Router#', 5)

    def Clear_Port_on_Terminal(self, line_start, line_end):
        """
        清除 line
        """
        for line in range(line_start, line_end):  #清理line2 ~ line22
            self.connect.send_and_receive(f'clear line {line}', '[confirm]', 5)
            self.connect.send_and_receive('', 'Router#', 5)


''' class Gemini_Test_Item(metaclass = myMetaClass):

    Variable = Global_Variable.DUT_Variable()
    
    def __init__(self, **args):
        global Variable
        Variable = args['Variable']
        self.check_test = Test_item_check.Gemini_Test(self.Variable, args['value_config_path'])
        self.connect = Telnet(args['ip'], args['port'], args['logger'], self.Variable)
        self.port = args['port']
        self.Variable.logger = args['logger']
        self.root_word = 'root@intel-corei7-64:~/mfg#'
    

    def Check_Telnet_Connect(self):
        """
        確認是否能連上dut
        """
        self.connect.check_connect()
    
    
    def Boot_Up(self):
        """
        dut開機
        """
        self.connect.send_and_receive(None, self.root_word, 150)

    
    def Set_Two_Power(self):
        """
        切換雙電源供電
        """
        self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
        self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
        self.check_test.check_two_power_address()
        self.connect.send_and_receive('i2cset -y 0 0x72 0x0 0x0', self.root_word, 5)
        self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x0', self.root_word, 5)
    
    def Set_A_Power(self):
        """
        切換A電源供電
        """
        self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
        self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
        self.check_test.check_two_power_address()
        self.connect.send_and_receive('i2cset -y  0 0x73 0x0 0x2', self.root_word, 5)
        self.connect.send_and_receive('i2cset -y  0 0x75 0x15 0x20', self.root_word, 5)
        self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
        self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
        self.check_test.check_A_power_address()


    def Set_B_Power(self):
        """
        切換B電源供電
        """
        self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
        self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
        self.check_test.check_two_power_address()
        self.connect.send_and_receive('i2cset -y  0 0x73 0x0 0x2', self.root_word, 5)
        self.connect.send_and_receive('i2cset -y  0 0x75 0x15 0x10', self.root_word, 5)
        self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
        self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
        self.check_test.check_B_power_address()
    

    def Check_HW_SW_Ver(self):
        """
        檢查SW 和 HW 版本
        """
        self.connect.send_and_receive('./show_version', self.root_word, 30)
        self.check_test.check_HW_SW()
    
    def Check_RTC(self):
        """
        檢查RTC資訊
        """
        self.connect.send_and_receive('hwclock', self.root_word, 5)
        self.check_test.check_RTC()
    
    def Check_HW_Monitor(self):
        """
        檢查HW monitor(電壓, 風扇轉速, 風扇Alert, Temperature, Temperature Alert, CPU core Temperature PSU (0x58) Alert Status Check, PSU (0x59) Alert Status Check)
        """
        self.Variable.logger.debug(f"port [{self.port}] in [check_HW_monitor]")
        self.connect.send_and_receive('./hw_monitor', self.root_word, 60)
        self.check_test.HW_Monitor()

    def Check_Fan0_Speed(self):
        """
        檢查在風扇0%的情況下風扇轉速是否正常
        """
        self.Variable.logger.debug(f"port [{self.port}] in [Check_Fan_Speed_0]")
        self.connect.send_and_receive('./mfg_sources/fan_control.sh speed 0', self.root_word, 10)
        time.sleep(5)
        self.connect.send_and_receive('./mfg_sources/fan_monitor.sh', self.root_word, 20)
        self.check_test.check_Fan_0()


    def Check_Fan100_Speed(self):
        """
        檢查在風扇100%的情況下風扇轉速是否正常
        """
        self.Variable.logger.debug(f"port [{self.port}] in [Check_Fan_Speed_100]")
        self.connect.send_and_receive('./mfg_sources/fan_control.sh speed 100', self.root_word, 10)
        time.sleep(5)
        self.connect.send_and_receive('./mfg_sources/fan_monitor.sh', self.root_word, 20)
        self.check_test.check_Fan_100()
    

    def DRAM_Test(self):
        """
        DRAM測試
        """
        self.Variable.logger.debug(f"port [{self.port}] in [DRAM_Test]")
        self.connect.send_and_receive('./mfg_sources/DDR_test.sh 16 1', self.root_word, 60)
        self.check_test.check_DRAM_test()

    
    def SSD_Test(self):
        """
        SSD測試
        """
        self.Variable.logger.debug(f"port [{self.port}] in [SSD_Test]")
        self.connect.send_and_receive('./mfg_sources/peripheralTest_sequential.sh 64 0 SSD', self.root_word, 10)
        self.check_test.check_SSD_test()
    
    def Module_Signal_Check(self):
        """
        確認各模組的信號
        """
        self.Variable.logger.debug(f"port [{self.port}] in [Module_Signal_Check]")
        self.connect.send_and_receive('./mfg_sources/factory_mb_module_connection_check.sh', self.root_word, 180)
        self.check_test.check_module_signal()

    def Set_Loopback_3_5W(self):
        """
        將各loopback module設定成3.5w
        """
        self.Variable.logger.debug(f"port [{self.port}] in [Set_Loopback_3_5W]")
        self.connect.send_and_receive('./mfg_sources/module_voltage_control.sh 3.5', self.root_word, 20)
        self.check_test.check_loopback_power()

    def Traffic_Test(self):
        """
        loopback測試初始化
        """
        self.Variable.logger.debug(f"port [{self.port}] in [Traffic_Test]")
        self.connect.send_and_receive('./appDemo', 'Console#', 120)
        self.check_test.check_traffic_test()

    def Loopbak_Test(self):
        """
        loopback測試
        """
        self.Variable.logger.debug(f"port [{self.port}] in [Loopbak_Test]")
        self.connect.send_and_receive('shell-execute PT_Pretest_Request 100 25 500', 'Console#', 40)
        self.check_test.check_loopback_test()
        self.connect.send_and_receive('CLIexit', '->', 5)
        self.connect.send_and_receive('exit', self.root_word, 5) '''


    
    
    
    




if "__main__" == __name__:
    a = Terminal_Server_Test_Item(port = 'COM7', baud = 9600, station = 'terminal')
    a.enter_en_mode()
    a.clear_port_on_terminal(2,23)

    ''' time_ = 10
    A1 = EZ1K_A1_Test_Item(ip = "10.1.1.2", port = 2002, station = 'dut')
    A1.connect_dut()
    A1.boot_up()
    A1.enter_swtich_mode()
    A1.load_vlan(8)
    A1.clear_counter()
    A1.check_counter()
    A1.disconnect_dut() '''
    
    