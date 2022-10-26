from copy import deepcopy
from tkinter import N
from Log_Dealer import Log_Model, Upload_Log_Tranfer

class _Global_Flag():
    upload_func_open = False
    dut_been_test_fail = False

class SingleTon_Flag(_Global_Flag):
    _instance = None

    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance 
    
    def clear_all(self):
        self.upload_func_open = False
        self.dut_been_test_fail = False





class _comport_data():
    terminal_comport = str()

class _dut_data():

    _telnet_port = int()
    run_times = 1
    total_run_times = 5
    
    _dut_info = dict()
    _dut_test_fail = False
    _dut_error_code = str()
    
    _test_start_time = str()
    _test_end_time = str()

    
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

    ftp_upload_path = str()
    _device_id = None
    _op = None
    
    been_sfis_upload = False
    been_checkroute = False
    _check_route_fail = False
    _sfis_upload_fail = False

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, data:int):
        self._device_id = data

    @property
    def op(self):
        return self._op

    @op.setter
    def op(self, data:str):
        self._op = data
    
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
    _sys_error_msg = str()
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
        self._sys_error_msg += data

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


        
class _All_Variable(_error_msg, _dut_data, _online_data, _comport_data, _debug_logger, Upload_Log_Tranfer):
    
    VERSION = 'V0.00.01'
    open_log = True
    log_model = Log_Model.no_name_no_time
    
    _debug_logger = None 
    _tmp_log = str()
    _log_raw_data = dict()
    _log = str()
    _upload_data = dict()
    _sfis_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{VERSION}\r\n'
    _iplas_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{VERSION}\r\n'
    _form_log = ['<Item>', '<Result>', '<Value>', '<Upper>', '<Lower>', '<Error>', '<Time>']

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
        self._test_error_msg = str()
        self._dut_info = dict()
        self._dut_error_code = str()
        self._sys_error_msg = str()
        self._ftp_error_msg = str()
        self._sfis_error_msg = str()
        self._iplas_error_msg = str()
        self._check_route_fail = False
        self._sfis_upload_fail = False
        self._test_start_time = str()
        self._test_end_time = str()
        self._tmp_log = str()
        self._dut_test_fail = False
        self._log_raw_data = dict()
        self._log = str()
        self._upload_data = dict()
        self._sfis_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{self.VERSION}\r\n'
        self._iplas_log = f'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,{self.VERSION}\r\n'
        self._form_log = ['<Item>', '<Result>', '<Value>', '<Upper>', '<Lower>', '<Error>', '<Time>']



        
if "__main__" == __name__:
    pass
