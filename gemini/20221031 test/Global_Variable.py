from copy import deepcopy
import threading
from Log_Dealer import Log_Model, Upload_Log_Tranfer

class _Global_Variable():
    VERSION = 'V0.00.01'    #程式版本
    log_model = Log_Model.no_name_no_time   #log存取的型態
    UI_Signal = None

    online_function = False
    sfis_deviceID_list = ['992632', '992631', '992630', '992629', '992628', '992627', '992626', '992625', '992624', '992622',
                        '992632', '992631', '992630', '992629', '992628', '992627', '992626', '992625', '992624', '992622']
    
    value_config_path = r".\value_config.ini"
    config_path = r'.\config.ini'

    log_root_path = r'.\log'
    logger_path = r'.\debug'

    telnet_ip = "10.1.1.2"

    serial_name = 'Gemini'
    test_time = 8
    terminal_comport = 'COM7'
    open_station = [2002, 2003, 2004]
    ftp_upload_path = '/SWITCH'
    op ='LA2100645'

    total_run_times = 1  #總共需要跑幾次

    main_debug_logger = None
    

class SingleTon_Global(_Global_Variable):
    """
    整個程式的全域變數
    """
    _instance = None

    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance 
    


''' class SingleTone_local(dict):  
    def __new__(cls):
        ident = threading.get_ident()
        if not hasattr(cls, '_variable'):
            cls._variable = super(SingleTone_local, cls).__new__(cls)
        if ident not in cls._variable:
            cls._variable[ident] = super(SingleTone_local, cls).__new__(cls, ident)
        return cls._variable
    
    
    def create_variable(self):
        ident = threading.get_ident()
        v = Thread_variable_dic()
        add_variable(self._variable[ident], v.thread_global)
        add_variable(self._variable[ident], v.thread_local)

    def init_variable(self):
        ident = threading.get_ident()
        v = Thread_variable_dic()
        add_variable(self._variable[ident], v.thread_local)
         '''

"""
有底線的變數為每次新的一輪測試都會被清掉的變數
"""

''' class Thread_variable_dic():

    v = SingleTon_Global()
    thread_global = {'dut_been_test_fail' : False,
                        'telnet_port' : int(),
                        'run_times' : 1,  #跑到第幾次
                        'device_id' : None,    #測試時這個dut的device_id (SFIS)
                        'DUT_SFIS_SN' : str(),
                        'been_checkroute' : False,     #是否曾經check route過
                        'been_sfis_upload' : False,     #是否曾經上傳過SFIS
                        'main_debug_logger' : None,
                        'dut_debug_logger' : None,
                        'upload_debug_logger' : None,
                        'sys_debug_logger' : None

                    }
    
    thread_local = {'_dut_info' : dict(), #dut的資料，包含SN、機種...
                        '_dut_test_fail' : False, #這輪測試是否失敗
                        '_dut_error_code' : str(), #測項失敗的error code
                        '_test_item_start_timer' : float(), #這個測項開始的時間(計時器)(time.time())
                        '_test_start_time' : str(), #這次測試開始的時間
                        '_test_end_time' : str(),  #這次測試結束的時間
                        '_ftp_local_path' : str(), 
                        '_ftp_remote_path' : str(),
                        '_iplas_log_path' : str(),
                        '_check_route_fail' : False,   #這次測試是否check route 失敗
                        '_sfis_upload_fail' : False,   #這次測試是否sfis上傳失敗
                        '_test_error_msg' : str(),
                        '_sys_error_msg' : list(),
                        '_ftp_error_msg' : str(),
                        '_sfis_error_msg' : str(),
                        '_iplas_error_msg' : str(),
                        '_debug_logger' : None,
                        '_tmp_log' : str(), #暫存的log檔 (在每下一次指令後收到的資料都會先存到這裡，用於測項判斷時可以拿取)
                        '_log_raw_data' : dict(), #原始log資料 ({'start_time': '', 'log':'', 'end_time': ''})
                        '_log' : str(),  #被加總之後的log，型態取決於前面的設定
                        '_upload_data' : dict(), #上傳的log的原始型態 ({test name: 1/0, value, lower, upper, error, time})
                        '_sfis_log' : f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{self.v.VERSION}\r\n',
                        '_iplas_log' : f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{self.v.VERSION}\r\n',
                        '_form_log' : [['<Item>', '<Result>', '<Value>', '<Upper>', '<Lower>', '<Error>', '<Time (s)>']],

                        }
    """在一個thread中的全域變數""" '''
    


def add_variable(dic:dict, variable:dict):
    for name, value in variable.items():
        dic[name] = value



class _dut_data():
    _telnet_port = int() 
    run_times = 1  #跑到第幾次
    total_run_times = 5  #總共需要跑幾次
    
    _dut_info = dict() #dut的資料，包含SN、機種...
    _dut_test_fail = False #這輪測試是否失敗
    _dut_error_code = str() #測項失敗的error code

    _test_item_start_timer = float() #這個測項開始的時間(計時器)(time.time())
    
    _test_start_time = str() #這次測試開始的時間
    _test_end_time = str()  #這次測試結束的時間

    
    @property
    def dut_info(self):
        return self._dut_info

    @dut_info.setter
    def dut_info(self, data:dict):
        self._dut_info.update(data)
    
    @property
    def dut_test_fail(self):
        return self._dut_test_fail

    @dut_test_fail.setter
    def dut_test_fail(self, data:bool):
        self._dut_test_fail = data
    
    @property
    def error_code(self):
        return self._dut_error_code

    @error_code.setter
    def error_code(self, data:str):
        self._dut_error_code = data

    @property
    def telnet_port(self):
        return self._telnet_port

    @telnet_port.setter
    def telnet_port(self, data:int):
        self._telnet_port = data
    
    @property
    def test_item_start_timer(self):
        return self._test_item_start_timer

    @test_item_start_timer.setter
    def test_item_start_timer(self, data:float):
        self._test_item_start_timer = data

    @property
    def test_start_time(self):
        return self._test_start_time

    @test_start_time.setter
    def test_start_time(self, data:str):
        self._test_start_time = data

    @property
    def test_end_time(self):
        return self._test_end_time

    @test_end_time.setter
    def test_end_time(self, data:str):
        self._test_end_time = data
    
class _online_data():
    _ftp_local_path = str()
    _ftp_remote_path = str()

    _device_id = str()   #測試時這個dut的device_id (SFIS)
    
    been_checkroute = False     #是否曾經check route過
    been_sfis_upload = False     #是否曾經上傳過SFIS
    
    _check_route_fail = False   #這次測試是否check route 失敗
    _sfis_upload_fail = False   #這次測試是否sfis上傳失敗

    @property
    def ftp_local_path(self):
        return self._ftp_local_path

    @ftp_local_path.setter
    def ftp_local_path(self, data:str):
        self._ftp_local_path = data
    
    @property
    def ftp_remote_path(self):
        return self._ftp_remote_path

    @ftp_remote_path.setter
    def ftp_remote_path(self, data:str):
        self._ftp_remote_path = data


    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, data:str):
        self._device_id = data

    
    @property
    def check_route_fail(self):
        return self._check_route_fail

    @check_route_fail.setter
    def check_route_fail(self, data:bool):
        self._check_route_fail = data
    
    @property
    def sfis_upload_fail(self):
        return self._sfis_upload_fail

    @sfis_upload_fail.setter
    def sfis_upload_fail(self, data:bool):
        self._sfis_upload_fail = data
    
class _error_msg():

    _test_error_msg = str()
    _sys_error_msg = list()
    _ftp_error_msg = str()
    _sfis_error_msg = str()
    _iplas_error_msg = str()

    @property
    def test_error_msg(self):
        return self._test_error_msg

    @test_error_msg.setter
    def test_error_msg(self, data:str):
        self._test_error_msg += data
    
    @property
    def sys_error_msg(self):
        return self._sys_error_msg

    @sys_error_msg.setter
    def sys_error_msg(self, data:str):
        self._sys_error_msg.append(data)

    @property
    def ftp_error_msg(self):
        return self._ftp_error_msg

    @ftp_error_msg.setter
    def ftp_error_msg(self, data:str):
        self._ftp_error_msg = data
    
    @property
    def sfis_error_msg(self):
        return self._sfis_error_msg

    @sfis_error_msg.setter
    def sfis_error_msg(self, data:str):
        self._sfis_error_msg = data
    
    @property
    def iplas_error_msg(self):
        return self._iplas_error_msg

    @iplas_error_msg.setter
    def iplas_error_msg(self, data:str):
        self._iplas_error_msg = data

class _debug_logger():

    dut_debug_logger = None
    upload_debug_logger = None
    sys_debug_logger = None

    _debug_logger = None #暫存的debug logger(作為切換logger用)

    @property
    def debug_logger(self):
        return self._debug_logger

    @debug_logger.setter
    def debug_logger(self, data):
        self._debug_logger = data
     
class All_Variable(_error_msg, _dut_data, _online_data, _debug_logger, Upload_Log_Tranfer):
    

    VERSION = 'V0.00.01'    #程式版本
    open_log = True     #是否開啟存取log
    log_model = Log_Model.no_name_no_time   #log存取的型態
        
    dut_been_test_fail = False
    _tmp_log = str() #暫存的log檔 (在每下一次指令後收到的資料都會先存到這裡，用於測項判斷時可以拿取)
    _log_raw_data = dict() #原始log資料 ({'start_time': '', 'log':'', 'end_time': ''})
    _log = str()  #被加總之後的log，型態取決於前面的設定
    _upload_data = dict() #上傳的log的原始型態 ({test name: 1/0, value, lower, upper, error, time})
    _sfis_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{VERSION}\r\n'
    _iplas_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{VERSION}\r\n'
    _form_log = [['<Item>', '<Result>', '<Value>', '<Upper>', '<Lower>', '<Error>', '<Time>']]

    @property
    def debug_logger(self):
        return self._debug_logger

    @debug_logger.setter
    def debug_logger(self, logg):
        self._debug_logger = logg
    
    @property
    def tmp_log(self):
        return self._tmp_log

    @tmp_log.setter
    def tmp_log(self, data:str):
        self._tmp_log = data

    @property
    def raw_log(self):
        return self._log_raw_data   
        
    @raw_log.setter
    def raw_log(self, datas:dict):
    
        if self.open_log:
            temp_log = dict()
            if datas.get('name'):
                self.test_name = datas.pop('name')
                if self.test_name not in self._log_raw_data:
                    self._log_raw_data[self.test_name] = [None, '', None]

            for key, value in datas.items():
                if key == 'start_time':
                    self._log_raw_data[self.test_name][0] = value
                
                if key == 'log':
                    self._log_raw_data[self.test_name][1] += value
                    self._tmp_log = value

                if key == 'end_time':
                    self._log_raw_data[self.test_name][2] = value
                    temp_log[self.test_name] = deepcopy(self._log_raw_data[self.test_name])
                    self.log = self.log_model(temp_log)
    
                            
    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, data:str):
        if data:
            self._log += data

    @property
    def upload_log(self):
        return self._upload_data
    
    @upload_log.setter
    def upload_log(self, datas:tuple):
        temp_dic = dict()
        if self.open_log:
            test_item, tuple_value = datas   #tuple_value = (0/1, value, lower, upper, error, time)
            self._upload_data[test_item] = tuple_value
            temp_dic[test_item] = tuple_value
            self.sfis_log = self.transfer_to_sfis(temp_dic)
            self.iplas_log = self.transfer_to_iplas(temp_dic)
            self.form_log = self.transfer_to_form(temp_dic)

    @property
    def sfis_log(self):
        return self._sfis_log

    @sfis_log.setter    
    def sfis_log(self, data:str):
        self._sfis_log += data

    @property
    def iplas_log(self):
        return self._iplas_log

    @iplas_log.setter    
    def iplas_log(self, data:str):
        self._iplas_log += data
    
    @property
    def form_log(self):
        return self._form_log

    @form_log.setter    
    def form_log(self, data:list):
        for i in data:
            self._form_log.append(i)




def variable_setter(local):
    thread_global_set(local)
    thread_local_set(local)
    

def thread_global_set(local):
    local.log_model = Log_Model.no_name_no_time   #log存取的型態
    local.dut_been_test_fail = False
    local.telnet_port = int() 
    local.run_times = 1
    local.test_start_time = str()
    local.test_end_time = str()
    local.device_id = str()
    local.been_checkroute = False 
    local.been_sfis_upload = False 

def thread_local_set(local):
    local.log = str()
    local.tmp_log = str()
    local.raw_log = dict()
    local.upload_log = dict()
    local.sfis_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,V1.00.01\r\n'
    local.iplas_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,V1.00.01\r\n'
    local.form_log = [['<Item>', '<Result>', '<Value>', '<Upper>', '<Lower>', '<Error>', '<Time>']]
    local.dut_info = dict()
    local.dut_test_fail = False
    local.dut_error_code = str()
    local.test_item_start_timer = float()
    local.ftp_local_path = str()
    local.ftp_remote_path = str()
    local.check_route_fail = False
    local.sfis_upload_fail = False
    local.test_error_msg = str()
    local.sys_error_msg = list()
    local.ftp_error_msg = str()
    local.sfis_error_msg = str()
    local.iplas_error_msg = str()
    local.dut_debug_logger = None
    local.upload_debug_logger = None
    local.sys_debug_logger = None
    local.debug_logger = None
  



        
if "__main__" == __name__:
    pass
