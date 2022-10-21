
class Same_Variable():
    def __init__(self): 
        self.tmp_log = str()
        self._sys_error_msg = str()
        self._test_error_msg = str()
        self._upload_data = dict()

        self._logger = None 

    @property
    def upload_log(self):
        return self._upload_data
    
    @upload_log.setter
    def upload_log(self, datas:tuple):
        test_item, tuple_value = datas   #tuple_value = (0/1, value, lower, upper, error, time)
        self._upload_data[test_item] = tuple_value
 
    @property
    def sys_error_msg(self):
        return self._sys_error_msg

    @sys_error_msg.setter
    def sys_error_msg(self, data):
        self._sys_error_msg += data
    
    @property
    def test_error_msg(self):
        return self._test_error_msg

    @test_error_msg.setter
    def test_error_msg(self, data):
        self._test_error_msg += data

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logg):
        self._logger = logg


class Terminal_Variable(Same_Variable):
    def __init__(self):
        Same_Variable.__init__(self)
        self._terminal_log = str()

    @property
    def log(self):
        return self._terminal_log

    @log.setter
    def log(self, datas:str):
        self.tmp_log = datas
        self._terminal_log += datas

class DUT_Variable(Same_Variable):
    def __init__(self):
        super(DUT_Variable, self).__init__()
        self._dut_log = str()
    
    @property
    def dut_log(self):
        return self._dut_log
    
    @dut_log.setter
    def dut_log(self, datas:str):
        self.tmp_log = datas
        self._dut_log += datas

class Package_Variable(Same_Variable):
    def __init__(self):
        super(Package_Variable, self).__init__()
        self._package_machine_log = str()
    
    @property
    def pg_log(self):
        return self._package_machine_log   
        
    @pg_log.setter
    def pg_log(self, datas:str):
        self.tmp_log = datas
        self._package_machine_log += datas


if '__main__' == __name__:
    oo = Terminal_Variable()
    oo.log = 'lllll'
    print(oo.log)