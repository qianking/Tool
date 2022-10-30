import time
import sys
import traceback
from datetime import datetime
from functools import wraps
from comport_and_telnet import Telnet
from comport_and_telnet import COM
import Test_item_check
from Log_Dealer import Log_Model
from error_code import Error_Code
from Global_Variable import SingleTon_Variable, SingleTon_Flag
from exceptions import TimeOutError, TestItemFail, Test_Fail


class myMetaClass(type):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if not len(bases) and callable(value) and attr != '__init__':
                local[attr] = log_deco()(value)
        return super().__new__(cls, name, bases, local)
    
class log_deco():

    Flag = SingleTon_Flag()
    Variable = SingleTon_Variable()

    def __init__(self):
        self.ERROR = Error_Code()
        
    def get_runtime(self):
        runtime = str(time.time() - self.start_time)
        runtime = int(runtime.split('.')[0])
        return runtime

       
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            ''' test_item = func.__name__
            self.v.Variable.raw_log = {'name': test_item, 'start_time': datetime.now()}
            func(*args, **kwargs)
            self.v.Variable.raw_log = {'end_time': datetime.now()}
            return True '''
            try:
                self.start_time = time.time()
                test_item = func.__name__
                self.Variable.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
                self.Variable.raw_log = {'name': test_item, 'start_time': datetime.now()}

                func(*args, **kwargs)

            #當telnet或是 comport timeout時會進到這裡
            except TimeOutError:
                print('timeoutfail')
                self.error_function(test_item)
                raise Test_Fail
                
            
            #測試項目失敗會進到這裡
            except TestItemFail as test_item_data:
                print('testitemfail')
                self.error_function(test_item, test_item_data.args[0])
                raise Test_Fail
               

            #當發生系統性的錯誤時會進到這裡
            except Exception as ex:
                self.sys_exception(ex)
                raise Exception
            
            else:
                self.Variable.upload_log = (test_item, (1, None, None, None, None, self.get_runtime()))
            
            finally:
                self.Variable.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
                self.Variable.raw_log = {'end_time': datetime.now()}
        
        return decorated 

    def error_function(self, test_item, test_item_data = None):

        self.Variable.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')

        if test_item_data[0]:
            test_item = test_item_data[0]

        error = self.ERROR[test_item]
        self.Variable.error_code = error
        self.Flag.dut_been_test_fail = True
        self.Variable.dut_test_fail = True
        
        self.Variable.upload_log = (test_item, (0, test_item_data[1][0], test_item_data[1][1], test_item_data[1][2], error, self.get_runtime()))
        self.Variable.test_error_msg = test_item_data[2]

    def sys_exception(self, ex):

        #只有這三種錯誤式系統的exception，所以直接在UI彈出提示視窗   
        if 'FileNotFoundError' in str(ex):           #console連接錯誤 電腦找不到這個port口
            #print('Comport 找不到指定port口')
            self.Variable.sys_error_msg = 'Comport 找不到指定port口'
                
        elif 'PermissionError' in str(ex):             #console連接錯誤 port口被其他程式使用
            #print('Comport Port口被占据')
            self.Variable.sys_error_msg = 'Comport Port口被占据'
        
        elif 'WinError 10061' in str(ex):                    #telnet連接錯誤 telnet被占線
            #print('Telnet连线被占据')
            self.Variable.sys_error_msg = 'Telnet连线被占据'

        else:
            error_msg = self.error_dealer(ex)
            print(error_msg)
            self.Variable.sys_error_msg = error_msg
    
    def error_dealer(self, ex):
        error_class = ex.__class__.__name__ #取得錯誤類型
        detail = ex.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2]#取得發生的函數名稱
        errMsg = f"{[error_class]}\n\"{fileName}\", line {lineNum}, in {funcName}\n{detail}"
        return errMsg
          
class Terminal_Server_Test_Item(metaclass = myMetaClass):

    Variable = SingleTon_Variable()

    def __init__(self, **args):
        self.Variable.debug_logger = self.Variable.main_debug_logger
        self.connect = COM(args['port'], args['baud'], self.Variable)
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
        if self.check_test.If_PassWord(self.Variable.tmp_log):
            self.connect.send_and_receive('pega123', 'Router>', 5)            
        self.connect.send_and_receive('en', 'Router#', 5)

    def Clear_Port_on_Terminal(self, line_start, line_end):
        """
        清除 line
        """
        for line in range(line_start, line_end):
            self.connect.send_and_receive(f'clear line {line}', '[confirm]', 5)
            self.connect.send_and_receive('', 'Router#', 5)


class Gemini_Test_Item(metaclass = myMetaClass):

    Variable = SingleTon_Variable()

    def __init__(self, **args):
        self.Variable.debug_logger = self.Variable.dut_debug_logger
        self.connect = Telnet(args['ip'], args['port'], self.Variable)
        self.check_test = Test_item_check.Gemini_Test(self.Variable, args['value_config_path'])
        self.port = args['port']
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

    def Rebbot(self):
        """
        dut 重開機
        """
        self.connect.send_and_receive('reboot', 'Restarting system', 20)

    def Get_SN(self):
        """
        拿取機台SN
        """
        self.connect.send_and_receive('./mfg_sources/mb_eeprom_rw.sh r serial_number', self.root_word, 10)
        self.check_test.get_SN()
        
    
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
        self.connect.send_and_receive('./hw_monitor', self.root_word, 60)
        self.check_test.HW_Monitor()

    def Check_Fan0_Speed(self):
        """
        檢查在風扇0%的情況下風扇轉速是否正常
        """
        self.connect.send_and_receive('./mfg_sources/fan_control.sh speed 0', self.root_word, 10)
        time.sleep(5)
        self.connect.send_and_receive('./mfg_sources/fan_monitor.sh', self.root_word, 20)
        self.check_test.check_Fan_0()


    def Check_Fan100_Speed(self):
        """
        檢查在風扇100%的情況下風扇轉速是否正常
        """
        self.connect.send_and_receive('./mfg_sources/fan_control.sh speed 100', self.root_word, 10)
        time.sleep(5)
        self.connect.send_and_receive('./mfg_sources/fan_monitor.sh', self.root_word, 20)
        self.check_test.check_Fan_100()
    

    def DRAM_Test(self):
        """
        DRAM測試
        """
        self.connect.send_and_receive('./mfg_sources/DDR_test.sh 16 1', self.root_word, 60)
        self.check_test.check_DRAM_test()

    
    def SSD_Test(self):
        """
        SSD測試
        """
        self.connect.send_and_receive('./mfg_sources/peripheralTest_sequential.sh 64 0 SSD', self.root_word, 10)
        self.check_test.check_SSD_test()
    
    def Module_Signal_Check(self):
        """
        確認各模組的信號
        """
        self.connect.send_and_receive('./mfg_sources/factory_mb_module_connection_check.sh', self.root_word, 180)
        self.check_test.check_module_signal()

    def Set_Loopback_3_5W(self):
        """
        將各loopback module設定成3.5w
        """
        self.connect.send_and_receive('./mfg_sources/module_voltage_control.sh 3.5', self.root_word, 20)
        self.check_test.check_loopback_power()

    def Traffic_Test(self):
        """
        loopback測試初始化
        """
        self.connect.send_and_receive('./appDemo', 'Console#', 120)
        self.check_test.check_traffic_test()

    def Loopbak_Test(self):
        """
        loopback測試
        """
        self.connect.send_and_receive('shell-execute PT_Pretest_Request 100 25 500', 'Console#', 40)
        self.check_test.check_loopback_test()
        self.connect.send_and_receive('CLIexit', '->', 5)
        self.connect.send_and_receive('exit', self.root_word, 5) 


    
    
    
    




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
    
    