from copy import deepcopy
from Log_Dealer import Log_Model, Upload_Log_Tranfer


class SingleTon_Variable():  
    def __new__(cls, *args, **kwargs): 
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.Variable = All_Variable()


class _dut_msg():
    def __init__(self):
        self._test_error_msg = str()
        self._dut_info = dict()
        self._dut_error_code = str()
        self._telnet_port = int()

    @property
    def test_error_msg(self):
        return self._test_error_msg

    @test_error_msg.setter
    def test_error_msg(self, data:str):
        self._test_error_msg += data
    
    @property
    def dut_info(self):
        return self._dut_info

    @dut_info.setter
    def dut_info(self, data:tuple):
        name, value = data
        self._dut_info[name] = value
    
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

class _error_msg():
    def __init__(self):
        self._sys_error_msg = str()
        self._ftp_error_msg = str()
        self._sfis_error_msg = str()
        self._iplas_error_msg = str()
    
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


        
class All_Variable(_error_msg, _dut_msg):
    
    test_name = None
    open_log = True
    log_model = Log_Model.no_name_time
    upload_flag = False


    def __init__(self, ): 
        _error_msg.__init__(self)
        _dut_msg.__init__(self)

        self._logger = None 
        self.tmp_log = str()
        self._log_raw_data = dict()
        self._log = str()
        self._upload_data = dict()
        self._sfis_log = str()
        self._iplas_log = str()


    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logg):
        self._logger = logg


    @property
    def raw_log(self):
        return self._log_raw_data   
        
    @raw_log.setter
    def raw_log(self, datas:dict):
    
        if self.open_log:
            temp_log = dict()
            if datas.get('name'):
                self.test_name = datas.pop('name')
                if datas['name'] not in self._log_raw_data:
                    self._log_raw_data[self.test_name] = []
                    
            for key, value in datas.items():
                self._log_raw_data[self.test_name].append(value)
                if key == 'log':
                    self.tmp_log = datas

                if key == 'end_time':
                    temp_log[self.test_name] = deepcopy(self._log_raw_data[self.test_name])
                    self.log = self.log_model(temp_log)
    
                            
    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, data:str):
        self._log += data

 
    @property
    def upload_log(self):
        return self._upload_data
    
    @upload_log.setter
    def upload_log(self, datas:tuple):
        if self.open_log:
            test_item, tuple_value = datas   #tuple_value = (0/1, value, lower, upper, error, time)
            self._upload_data[test_item] = tuple_value


    @property
    def sfis_log(self):
        return self._sfis_log

    @sfis_log.setter    
    def sfis_log(self, data:str()):
        self._sfis_log += data

    @property
    def iplas_log(self):
        return self._iplas_log

    @iplas_log.setter    
    def iplas_log(self, data:str()):
        self._iplas_log += data

    
    class Log_Title():

        title_data = {'program_version' : 'V1.00.10', 
                    'test_result' : 'Pass',
                    'error_code' : '',
                    'csn' : '',
                    'terminal_connect_flag' : 'Pass',
                    'start_time' : '',
                    'end_time' : ''}
        


        





if '__main__' == __name__:
    oo = Terminal_Variable()
    oo.log = 'lllll'
    print(oo.log)