import time
import threading
from datetime import datetime
from functools import wraps
from comport_and_telnet import Telnet
from comport_and_telnet import COM
import Test_item_check
import analyze_method
from Global_Variable import SingleTon_Global
import exceptions
from exceptions import TimeOutError, TestItemFail, Test_Fail



          
class Terminal_Server_Test_Item():

    G = SingleTon_Global()

    def __init__(self, l, **args):
        self.l = l
        self.l.debug_logger = self.G.main_debug_logger
        self.connect = COM(args['port'], args['baud'], self.l.debug_logger, self.l)
        self.l.debug_logger.debug(f"{'In Terminal Server':-^50}")
    
    def sys_exception(self, ex, l):
        error_msg = exceptions.error_dealer(ex)
        l.sys_error_msg.append(error_msg)
        print(error_msg)

    def Check_Comport(self): 
        """
        開啟並確認是否能連上Terminal server
        """
        test_item = 'Check_Comport'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            self.connect.check_connect()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
        

    def Enter_en_Mode(self):
        """
        進入Router#，如果有密碼就打密碼:pega123
        """
        test_item = 'Enter_en_Mode'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            self.connect.send_and_receive('', 'Router', 100, 'Password:')
            if analyze_method.Find_Method.FindString(self.l.tmp_log, 'Password:'):
                self.connect.send_and_receive('pega123', 'Router>', 5)            
            self.connect.send_and_receive('en', 'Router#', 5)
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
        
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
        

    def Clear_Port_on_Terminal(self, line_start, line_end):
        """
        清除 line
        """
        test_item = 'Clear_Port_on_Terminal'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            for line in range(line_start, line_end):
                self.connect.send_and_receive(f'clear line {line}', '[confirm]', 5)
                self.connect.send_and_receive('', 'Router#', 5)
            
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
        
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')





class Gemini_Test_Item():

    def __init__(self, l, **args):
        self.l = l
        self.l.debug_logger = self.l.dut_debug_logger
        self.connect = Telnet(args['ip'], args['port'], self.l.debug_logger, self.l)
        self.check_test = Test_item_check.Gemini_Test(self.l)
        self.port = args['port']
        self.root_word = 'root@intel-corei7-64:~/mfg#'

        self.l.debug_logger.debug(f"{self.l.run_times:-^50}")

    def sys_exception(self, ex, l):
        error_msg = exceptions.error_dealer(ex)
        l.sys_error_msg.append(error_msg)
        print(error_msg)

    def Check_Telnet_Connect(self):
        """
        確認是否能連上dut
        """
        test_item = 'Check_Telnet_Connect'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.check_connect()

        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False,
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
    
    def Boot_Up(self):
        """
        dut開機
        """
        test_item = 'Boot_Up'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive(None, self.root_word, 150)

        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')

    def Rebbot(self):
        """
        dut 重開機
        """
        test_item = 'Boot_Up'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('reboot', 'Restarting system', 20)
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')

    def Get_SN(self):
        """
        拿取機台SN
        """
        test_item = 'Get_SN'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('./mfg_sources/mb_eeprom_rw.sh r serial_number', self.root_word, 10)
            self.check_test.get_SN()

        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
        
    
    def Set_Two_Power(self):
        """
        切換雙電源供電
        """
        test_item = 'Boot_Up'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            
            self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
            self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
            self.check_test.check_two_power_address()
            self.connect.send_and_receive('i2cset -y 0 0x72 0x0 0x0', self.root_word, 5)
            self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x0', self.root_word, 5)

        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
    
    def Set_A_Power(self):
        """
        切換A電源供電
        """
        test_item = 'Boot_Up'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
            self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
            self.check_test.check_two_power_address()
            self.connect.send_and_receive('i2cset -y  0 0x73 0x0 0x2', self.root_word, 5)
            self.connect.send_and_receive('i2cset -y  0 0x75 0x15 0x20', self.root_word, 5)
            self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
            self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
            self.check_test.check_A_power_address()

        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')


    def Set_B_Power(self):
        """
        切換B電源供電
        """
        test_item = 'Set_B_Power'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
            self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
            self.check_test.check_two_power_address()
            self.connect.send_and_receive('i2cset -y  0 0x73 0x0 0x2', self.root_word, 5)
            self.connect.send_and_receive('i2cset -y  0 0x75 0x15 0x10', self.root_word, 5)
            self.connect.send_and_receive('i2cset -y 0 0x73 0x0 0x2', self.root_word, 5)
            self.connect.send_and_receive('i2cget -y 0 0x75 0x15', self.root_word, 5)
            self.check_test.check_B_power_address()

        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')

    def Check_HW_SW_Ver(self):
        """
        檢查SW 和 HW 版本
        """
        test_item = 'Check_HW_SW_Ver'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            self.connect.send_and_receive('./show_version', self.root_word, 30)
            self.check_test.check_HW_SW()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True

        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
    
    def Check_RTC(self):
        """
        檢查RTC資訊
        """
        test_item = 'Check_RTC'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('hwclock', self.root_word, 5)
            self.check_test.check_RTC()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
    
    def Check_HW_Monitor(self):
        """
        檢查HW monitor(電壓, 風扇轉速, 風扇Alert, Temperature, Temperature Alert, CPU core Temperature PSU (0x58) Alert Status Check, PSU (0x59) Alert Status Check)
        """
        test_item = 'Check_HW_Monitor'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('./hw_monitor', self.root_word, 60)
            self.check_test.HW_Monitor()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')

    def Check_Fan0_Speed(self):
        """
        檢查在風扇0%的情況下風扇轉速是否正常
        """
        test_item = 'Check_Fan0_Speed'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('./mfg_sources/fan_control.sh speed 0', self.root_word, 10)
            time.sleep(5)
            self.connect.send_and_receive('./mfg_sources/fan_monitor.sh', self.root_word, 20)
            self.check_test.check_Fan_0()

        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')


    def Check_Fan100_Speed(self):
        """
        檢查在風扇100%的情況下風扇轉速是否正常
        """
        test_item = 'Check_Fan100_Speed'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('./mfg_sources/fan_control.sh speed 100', self.root_word, 10)
            time.sleep(5)
            self.connect.send_and_receive('./mfg_sources/fan_monitor.sh', self.root_word, 20)
            self.check_test.check_Fan_100()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')

    

    def DRAM_Test(self):
        """
        DRAM測試
        """
        test_item = 'DRAM_Test'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('./mfg_sources/DDR_test.sh 16 1', self.root_word, 60)
            self.check_test.check_DRAM_test()

        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
    
    def SSD_Test(self):
        """
        SSD測試
        """
        test_item = 'SSD_Test'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            self.connect.send_and_receive('./mfg_sources/peripheralTest_sequential.sh 64 0 SSD', self.root_word, 10)
            self.check_test.check_SSD_test()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')
    
    def Module_Signal_Check(self):
        """
        確認各模組的信號
        """
        test_item = 'Module_Signal_Check'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('./mfg_sources/factory_mb_module_connection_check.sh', self.root_word, 180)
            self.check_test.check_module_signal()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')


    def Set_Loopback_3_5W(self):
        """
        將各loopback module設定成3.5w
        """
        test_item = 'Set_Loopback_3_5W'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:

            self.connect.send_and_receive('./mfg_sources/module_voltage_control.sh 3.5', self.root_word, 20)
            self.check_test.check_loopback_power()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
            
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')

    def Traffic_Test(self):
        """
        loopback測試初始化
        """
        test_item = 'Traffic_Test'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            self.connect.send_and_receive('./appDemo', 'Console#', 120)
            self.check_test.check_traffic_test()
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False

        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')

    def Loopbak_Test(self):
        """
        loopback測試
        """
        test_item = 'Loopbak_Test'
        self.l.debug_logger.debug(f'>>>>> In [{test_item}] <<<<<')
        self.l.test_item_start_timer = time.time()
        self.l.raw_log[test_item] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        try:
            self.connect.send_and_receive('shell-execute PT_Pretest_Request 100 25 500', 'Console#', 40)
            self.check_test.check_loopback_test()
            self.connect.send_and_receive('CLIexit', '->', 5)
            self.connect.send_and_receive('exit', self.root_word, 5) 
        
        except (TimeOutError,TestItemFail) :
            self.l.debug_logger.debug(f'>>>>> Failed In [{test_item}] <<<<<')
            return False
        
        #當發生系統性的錯誤時會進到這裡
        except Exception as ex:
            if len(str(ex)):
                self.sys_exception(ex, self.l)
            raise Exception
        
        else:
            return True
        
        finally:
            self.l.raw_log[test_item]['end_time'] = datetime.now()
            self.l.debug_logger.debug(f'>>>>> Out [{test_item}] <<<<<')


    
    
    
    




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
    
    