from copy import deepcopy
from tkinter import N
from Log_Dealer import Log_Model, Upload_Log_Tranfer

class _Global_Variable():
    upload_func_open = False
    dut_been_test_fail = False
    sfis_deviceID_list = ['992632', '992631', '992630', '992629', '992628', '992627', '992626', '992625', '992624', '992622',
                        '992632', '992631', '992630', '992629', '992628', '992627', '992626', '992625', '992624', '992622']
    value_config_path = r".\value_config.ini"





class SingleTon_Global(_Global_Variable):
    """
    整個測試都不會改變的flag
    """
    _instance = None

    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance 
    
    def clear_all(self):
        self.upload_func_open = False
        self.dut_been_test_fail = False


"""
有底線的變數為每次新的一輪測試都會被清掉的變數
"""

class _connect_data():
    telnet_ip = "10.1.1.2"
    terminal_comport = str()


class _dut_data():
    telnet_port = int() 
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
        return self.telnet_port

    @telnet_port.setter
    def telnet_port(self, data:int):
        self.telnet_port = data
    
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

    ftp_upload_path = str()     #需要上傳到的FTP位置
    _ftp_local_path = str()
    _ftp_remote_path = str()

    device_id = None    #測試時這個dut的device_id (SFIS)
    op = None   #整個測試時的OP (SFIS)
    
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
        return self.device_id

    @device_id.setter
    def device_id(self, data:int):
        self.device_id = data

    @property
    def op(self):
        return self.op

    @op.setter
    def op(self, data:str):
        self.op = data
    
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

    main_debug_logger = None
    terminal_debug_logger = None
    dut_debug_logger = None
    sfis_debug_logger = None
    ftp_debug_logger = None
    iplas_debug_logger = None

    _debug_logger = None

    @property
    def debug_logger(self):
        return self._debug_logger

    @debug_logger.setter
    def debug_logger(self, data):
        self._debug_logger = data


        
class _All_Variable(_error_msg, _dut_data, _online_data, _connect_data, _debug_logger, Upload_Log_Tranfer):
    
    VERSION = 'V0.00.01'    #程式版本
    open_log = True     #是否開啟存取log
    log_model = Log_Model.no_name_no_time   #log存取的型態
    
    _debug_logger = None #暫存的debug logger(作為切換logger用)
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



class SingleTon_Variable(_All_Variable):  

    _instance = None

    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance 
    
    def clear_all(self):
        """dut data"""
        self._dut_info = dict()
        self._dut_test_fail = False
        self._dut_error_code = str()
        self._test_item_start_timer = float()
        self._test_start_time = str()
        self._test_end_time = str()

        """online data"""
        self._ftp_local_path = str()
        self._ftp_remote_path = str()
        self._check_route_fail = False
        self._sfis_upload_fail = False

        """error msg"""
        self._test_error_msg = str()
        self._sys_error_msg = list()
        self._ftp_error_msg = str()
        self._sfis_error_msg = str()
        self._iplas_error_msg = str()

        """all variable"""
        self._debug_logger = None
        self._tmp_log = str()  
        self._log_raw_data = dict()
        self._log = str()
        self._upload_data = dict()
        self._sfis_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{self.VERSION}\r\n'
        self._iplas_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{self.VERSION}\r\n'
        self._form_log = [['<Item>', '<Result>', '<Value>', '<Upper>', '<Lower>', '<Error>', '<Time>']]



        
if "__main__" == __name__:
    pass
