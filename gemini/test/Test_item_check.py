from exceptions import TestItemFail
import re
import datetime
import traceback
import analyze_method
import read_ini
import sys
import exceptions
from functools import wraps
from error_code import Error_Code
from exceptions import TimeOutError
from Global_Variable import SingleTon_Variable, SingleTon_Flag


value_config_path = r"D:\Qian\python\NPI\Gemini\value_config.ini"

class Test_item_limit_Value():
    def __init__(self, value_config_path):
        self._config = read_ini.read_ini(value_config_path)
        #print(self._config)
    
    def __getitem__(self, data):
        test_item, test_name = data
        try: 
            upper_value = float(self._config[test_item][f"{test_name}_upper"])
            lower_value = float(self._config[test_item][f"{test_name}_lower"])
        except KeyError as ex:
            raise Exception(ex)
        else:
            return lower_value, upper_value

class myMetaClass(type):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if not len(bases) and callable(value) and attr != '__init__':
                local[attr] = Fail_Dealer()(value)
        return super().__new__(cls, name, bases, local)

class Fail_Dealer():
    v = SingleTon_Variable()
    f = SingleTon_Flag()

    def __init__(self):
        self.ERROR = Error_Code()

    def sys_exception(self, ex):
        error_msg = exceptions.error_dealer(ex)
        print(error_msg)
        self.v.sys_error_msg = error_msg
        self.upper_name = None
    
    def deal_result(self, results):
        flag = True
        
        for result in results:
            test_name = result[1]
            if not result[1]:  #如果test name為None，代表要使用上一層的func name
                test_name = self.upper_name
            if result[0]: #如果為PASS
                self.v.upload_log = (test_name, (1, result[2][0], result[2][1], result[2][2], None, None))
            else:
                flag = False
                temp = self.v.upload_log.get(test_name) #先接原有的log值出來
                temp = None if not temp else temp[5] #如果友直，那就將其設為 temp[5](test time)
                self.v.upload_log = (test_name, (0, result[2][0], result[2][1], result[2][2], self.ERROR[test_name], temp))

        return flag


    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
          
            try:
                self.upper_name = sys._getframe(1).f_code.co_name
                results = func(*args, **kwargs)
                flag = self.deal_result(results)  
                
                if not flag:
                    self.f.dut_been_test_fail = True
                    self.v.dut_test_fail = True
                    raise TestItemFail

            except Exception as ex:
                """系統錯誤"""
                self.sys_exception(ex)
                raise Exception 

            else:
                return True
        return decorated



class Gemini_Test(metaclass = myMetaClass):

    def __init__(self, Variable, value_config_path):
        self.Variable = Variable
        self.limit_value = Test_item_limit_Value(value_config_path)
    
    @staticmethod
    def _deal_test_name(test_name):
        test_name = test_name.strip('[').strip(']').lower()
        test_name = re.sub('[\[\]:]', ' ', test_name)
        test_name = '_'.join([i for i in test_name.split(' ') if i.strip() != ''])
        return test_name

    @staticmethod
    def _get_function_name():
        return traceback.extract_stack(None, 2)[0][2]

    def get_SN(self):
        tmp_log = list()
        SN = self.Variable.tmp_log.split('\r\n')[1]
        SN = SN.split(':')[1].strip()
        self.Variable.dut_info = {'SN' : SN}

        tmp_log.append((True, None, (SN, None, None)))
        return tmp_log


    def check_two_power_address(self):
        tmp_log = list()
        power_address = self.Variable.tmp_log.split('\r\n')[1]

        if power_address != '0x03':
            tmp_log.append((False, None, (power_address, None, None)))
        else:
            tmp_log.append((True, None, (power_address, None, None)))
        return tmp_log
    
    def check_A_power_address(self):
        tmp_log = list()
        power_address = self.Variable.tmp_log.split('\r\n')[1]

        if power_address != '0x22':
            tmp_log.append((False, None, (power_address, None, None)))
        else:
            tmp_log.append((True, None, (power_address, None, None)))
        return tmp_log
    
    def check_B_power_address(self):
        tmp_log = list()
        power_address = self.Variable.tmp_log.split('\r\n')[1]

        if power_address != '0x11':
            tmp_log.append((False, None, (power_address, None, None)))
        else:
            tmp_log.append((True, None, (power_address, None, None)))
        return tmp_log


    def check_HW_SW(self):
        tmp_log = list()
        HW_info = "Model name: FM6256-BNF"\
                "CPU: 8-core, Intel(R) Pentium(R) CPU D1517 @ 1.60GHz"\
                "MAC: Marvell Technology Group Ltd. Device 8400 , LnkSta: Speed 8GT/s , Width x2"\
                "DDR: 31.27 GB (32786348 kB)"\
                "SSD: ATA 256GB SATA Flash , 240GB"\
                "CPU Board : BDX-DE-BMC_NPU REV. 2.00"\
                "Main Board : GEMINI REV. 3.00"\
                "Fan Board : 5x40mm_FC_DB REV:2.00 , Maximum 5pcs Fan Modules ( FtB ) [ Board-ID : 0x57 ]"\
                "Fan Board EEPROM Info : 0x0957001f"
        find = analyze_method.Extract_Method.Extract_Data('Hardware Information(.*)Firmware Version', self.Variable.tmp_log)
        get_info = ''.join([i.strip() for i in find.strip().split('\r\n')])
        if get_info != HW_info:
            tmp_log.append((False, None, (None, None, None)))
            return tmp_log
        
        SW_info = "MFG: Gemini v0.2.7"\
                "SDK: Marvell CPSS 4.2.2020.3"\
                "Linux: 4.14.66-intel-pk-standard"\
                "BIOS: v5.11.1.3 , date: 01/25/2022"\
                "CPLD A (MB) - FW ver: 3  (HW ver value: 4 )"\
                "CPLD B (MB) - FW ver: 6  (HW ver value: 4 )"\
                "CPLD C (MB) - FW ver: 5  (HW ver value: 4 )"\
                "CPLD  (CPU) - FW ver: 6  (HW ver value: 3 )"\
                "MCU - Main Board: GEMINI (01001), ver. 0.11"\
                "MCU - Fan  Board: ver. 0.11"\
                "PMBus FW checksum (CPU 0x63) : 0x841e4474"\
                "PMBus FW checksum (CPU 0x64) : 0xd50129b2"\
                "PMBus FW checksum (MB  0x60) : 0x1b0ce447"\
                "PMBus FW checksum (MB  0x5F) : 0x1c51b6ac"\

        find = analyze_method.Extract_Method.Extract_Data('Firmware Version(.*)root@', self.Variable.tmp_log)            
        get_info = ''.join([i.strip() for i in find.strip().split('\r\n')])
        if get_info != SW_info:
            tmp_log.append((False, None, (None, None, None)))
            return tmp_log

        tmp_log.append((True, None, (None, None, None)))
        return tmp_log

    
    def check_RTC(self):
        tmp_log = list()
        find_year = int(analyze_method.Extract_Method.Extract_Data(' (\d{4}) ', self.Variable.tmp_log))
        now_date = datetime.date.today()

        if find_year != now_date.year:
            tmp_log.append((False, None, (find_year, None, None)))
        else:
            tmp_log.append((True, None, (find_year, None, None)))
        return tmp_log

    def HW_Monitor(self):
        #print(repr(self.Variable.tmp_log))
        tmp_log = list()
        #找到電壓資料
        count = 0
        check_item_name = 'adc'
        total_count = 9
        ADC_info = analyze_method.Extract_Method.Extract_Data('{ ADC }(.*?)\r\n\r\n\t*', self.Variable.tmp_log)            
        ADC_info = [i.strip() for i in ADC_info.split('\r\n') if i.strip() != '']
        for voltage_info in ADC_info:
            count += 1
            vol_name, vol_num = [i.strip() for i in voltage_info.split(':')]
            vol_num = analyze_method.Extract_Method.Get_Number(vol_num)
            vol_name = f"{check_item_name}_{self._deal_test_name(vol_name)}"

            check_limit = self.limit_value[self._get_function_name(), vol_name]

            if vol_num in range(check_limit[0], check_limit[1]):
                tmp_log.append((True, vol_name, (vol_num, check_limit[0], check_limit[1])))
            else:
                tmp_log.append((False, vol_name, (vol_num, check_limit[0], check_limit[1])))
                return tmp_log

        
        if count != total_count:
            tmp_log.append((False, None, (None, None, None)))
            return tmp_log
            
        
        #找到正常風扇轉速資料
        count = 0
        check_item_name = 'fannormal'
        total_count = 10
        Fan_info = analyze_method.Extract_Method.Extract_Data('{ \[Fan 1\] - \[Fan 5\] R.P.M }(.*?){', self.Variable.tmp_log) 
        Fan_info = [i.strip() for i in Fan_info.split('\r\n') if i.strip() != '']
        for fan_info in Fan_info:
            count += 1
            fan_name, fan_num = [i.strip() for i in fan_info.split(':')]
            fan_num = analyze_method.Extract_Method.Get_Number(fan_num)
            fan_name = f"{check_item_name}_{self._deal_test_name(fan_name)}"

            check_limit = self.config_value[self._get_function_name(), fan_name]
            if fan_num in range(check_limit[0], check_limit[1]):
                tmp_log.append((True, fan_name, (fan_num, check_limit[0], check_limit[1])))
            else:
                tmp_log.append((False, fan_name, (fan_num, check_limit[0], check_limit[1])))
                return tmp_log
        
        if count != total_count:
            tmp_log.append((False, None, (None, None, None)))
            return tmp_log


        #找到風扇警告資料
        check_item_name = 'fanalert_count'
        total_count = 40
        Fan_alert_info = analyze_method.Extract_Method.Extract_Data('{ \[Fan 1\] - \[Fan 5\] Alert }(.*?)\r\n\r\n\t*', self.Variable.tmp_log)
        count_N = len(re.findall(r'\sN\s', Fan_alert_info))
        if count_N == total_count:
            tmp_log.append((True, check_item_name, (count_N, total_count, total_count)))
        else:
            tmp_log.append((False, check_item_name, (count_N, total_count, total_count)))
            return tmp_log
         

        #找到各溫度資料
        count = 0
        check_item_name = 'npu_temperature'
        total_count = 4
        Temperature_info = analyze_method.Extract_Method.Extract_Data('{ Temperature }(.*?)\r\n\r\n\t*', self.Variable.tmp_log)
        Temperature_info = [i.strip() for i in Temperature_info.split('\r\n') if i.strip() != '']
        for temp_info in Temperature_info:
            count += 1
            temp_name, temp_num = [i.strip() for i in temp_info.split(':\t')]

            temp_num = analyze_method.Extract_Method.Get_Number(temp_num)
            temp_name = f"{check_item_name}_{self._deal_test_name(temp_name)}"

            check_limit = self.limit_value[self._get_function_name(), temp_name]
            if temp_num > check_limit[0] and temp_num < check_limit[1]:
                tmp_log.append((True, temp_name, (temp_num, check_limit[0], check_limit[1])))
            else:
                tmp_log.append((False, temp_name, (temp_num, check_limit[0], check_limit[1])))
                return tmp_log
        
        if count != total_count:
            tmp_log.append((False, None, (None, None, None)))
            return tmp_log


        #找到各溫度警告資料  
        count = 0  
        check_item_name = 'temperaturealert'
        total_count = 3
        Temperature_alert_info = analyze_method.Extract_Method.Extract_Data('{ Temperature Alert }(.*?)\r\n\r\n\t*', self.Variable.tmp_log)
        count_Normal = len(re.findall(r'\sNormal\s*', Temperature_alert_info))
        if count_Normal == total_count:
            tmp_log.append((True, check_item_name, (count_Normal, total_count, total_count)))
        else:
            tmp_log.append((False, check_item_name, (count_Normal, total_count, total_count)))
            return tmp_log


        #找到CPU溫度資料 
        count = 0  
        check_item_name = 'cpucoretemperature'
        total_count = 4
        crit_temp_lower = 10
        CPU_temperature_info = analyze_method.Extract_Method.Extract_Data('{ CPU core Temperature }(.*?)\r\n\r\n\t*', self.Variable.tmp_log)
        CPU_temperature_info = [i.strip() for i in CPU_temperature_info.split('\r\n') if i.strip() != '']
        for cpu_temp in CPU_temperature_info:
            count += 1
            cpu_name, cpu_temp_num = [i.strip() for i in cpu_temp.split(':')]
            crit_temp_upper = analyze_method.Extract_Method.Get_Number(cpu_temp_num.split('crit')[1])
            cpu_temp_num = analyze_method.Extract_Method.Get_Number(cpu_temp_num)

            if cpu_temp_num > crit_temp_lower and cpu_temp_num < crit_temp_upper:
                tmp_log.append((True, check_item_name, (cpu_temp_num, crit_temp_lower, crit_temp_upper)))
            else:
                tmp_log.append((False, check_item_name, (cpu_temp_num, crit_temp_lower, crit_temp_upper)))
                return tmp_log


        #找到各警告資料
        check_item_name = 'alertstatuecheck'
        Alert_status_info = analyze_method.Extract_Method.Extract_Data('\[MFG Msg\] PSU \(0x58\) Alert Status Check:(.*?)\r\n\r\n\t*', self.Variable.tmp_log)
        total_count = 32
        count_N = len(re.findall(r'---> N', Alert_status_info))
        if count_N == total_count:
            tmp_log.append((True, check_item_name, (count_N, total_count, total_count)))
        else:
            tmp_log.append((False, check_item_name, (count_N, total_count, total_count)))
            return tmp_log
        
        tmp_log.append((True, None, (None, None, None)))
        return tmp_log


    def check_Fan_0(self):
        tmp_log = list()
        count = 0
        check_item_name = 'fan0%'
        total_count = 10
        Fan_info = analyze_method.Extract_Method.Extract_Data('{ \[Fan 1\] - \[Fan 5\] R.P.M }(.*?){', self.Variable.tmp_log) 
        Fan_info = [i.strip() for i in Fan_info.split('\r\n') if i.strip() != '']
        for fan_info in Fan_info:
            count += 1
            fan_name, fan_num = [i.strip() for i in fan_info.split(':')]
            fan_num = analyze_method.Extract_Method.Get_Number(fan_num)
            fan_name = f"{check_item_name}_{self._deal_test_name(fan_name)}"

            check_limit = self.limit_value['Fan_Test', fan_name]
            if fan_num in range(check_limit[0], check_limit[1]):
                tmp_log.append((True, fan_name, (fan_num, check_limit[0], check_limit[1])))
            else:
                tmp_log.append((False, fan_name, (fan_num, check_limit[0], check_limit[1])))
                return tmp_log
        
        if count != total_count:
            tmp_log.append((False, None, (None, None, None)))
            return tmp_log

        tmp_log.append((True, None, (None, None, None)))
        return tmp_log

    def check_Fan_100(self):
        tmp_log = list()
        count = 0
        check_item_name = 'fan100%'
        total_count = 10
        Fan_info = analyze_method.Extract_Method.Extract_Data('{ \[Fan 1\] - \[Fan 5\] R.P.M }(.*?){', self.Variable.tmp_log) 
        Fan_info = [i.strip() for i in Fan_info.split('\r\n') if i.strip() != '']
        for fan_info in Fan_info:
            count += 1
            fan_name, fan_num = [i.strip() for i in fan_info.split(':')]
            fan_num = analyze_method.Extract_Method.Get_Number(fan_num)
            fan_name = f"{check_item_name}_{self._deal_test_name(fan_name)}"

            check_limit = self.limit_value['Fan_Test', fan_name]
            if fan_num in range(check_limit[0], check_limit[1]):
                tmp_log.append((True, fan_name, (fan_num, check_limit[0], check_limit[1])))
            else:
                tmp_log.append((False, fan_name, (fan_num, check_limit[0], check_limit[1])))
                return tmp_log
        
        if count != total_count:
            tmp_log.append((False, None, (None, None, None)))
            return tmp_log

        tmp_log.append((True, None, (None, None, None)))
        return tmp_log

    def check_DRAM_test(self):
        tmp_log = list()
        if 'DRAM Test PASS' not in self.Variable.tmp_log:
            tmp_log.append((False, None, (None, None, None)))
        else:
            tmp_log.append((True, None, (None, None, None)))
        return tmp_log


    def check_SSD_test(self):
        tmp_log = list()
        if 'SSD Test PASS' not in self.Variable.tmp_log:
            tmp_log.append((False, None, (None, None, None)))   
        else:
            tmp_log.append((True, None, (None, None, None)))
        return tmp_log

    def check_module_signal(self):
        tmp_log = list()
        total_count = 56
        signal_count = len(re.findall(r'All signal check OK', self.Variable.tmp_log))
        if signal_count != total_count:
            tmp_log.append((False, None, (signal_count, None, None)))
        else:
            tmp_log.append((True, None, (total_count, None, None)))
        return tmp_log

    def check_loopback_power(self):
        tmp_log = list()
        power_info = "Port 49 power is set to 0x1f (3.5 Watt)"\
                    "Port 50 power is set to 0x1f (3.5 Watt)"\
                    "Port 51 power is set to 0x1f (3.5 Watt)"\
                    "Port 52 power is set to 0x1f (3.5 Watt)"\
                    "Port 53 power is set to 0x1f (3.5 Watt)"\
                    "Port 54 power is set to 0x1f (3.5 Watt)"\
                    "Port 55 power is set to 0x1f (3.5 Watt)"\
                    "Port 56 power is set to 0x1f (3.5 Watt)"

        find = analyze_method.Extract_Method.Extract_Data('Module Power Setting ...(.*)root', self.Variable.tmp_log)
        get_info = ''.join([i.strip() for i in find.strip().split('\r\n')])

        if get_info != power_info:
            tmp_log.append((False, None, (None, None, None)))
        else:
            tmp_log.append((True, None, (None, None, None)))        
        return tmp_log 

    def check_traffic_test(self):
        tmp_log = list()
        if 'PEGATRON MFG Initial Ready' not in self.Variable.tmp_log:
            tmp_log.append((False, None, (None, None, None)))
        else:
            tmp_log.append((True, None, (None, None, None)))
        return tmp_log
    
    def check_loopback_test(self):
        tmp_log = list()
        if 'TOTAL TRAFFIC TEST RESULT: PASS' not in self.Variable.tmp_log:
            tmp_log.append((False, None, (None, None, None)))
        else:
            tmp_log.append((True, None, (None, None, None)))
        return tmp_log

    

        

           

