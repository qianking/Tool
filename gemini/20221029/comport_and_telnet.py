import time
import serial
import telnetlib
from functools import wraps
import sys
import time
import threading
import exceptions
from error_code import Error_Code
from exceptions import TimeOutError
from Global_Variable import SingleTone_local, SingleTon_Global

''' 
class myMetaClass(type):
    def __new__(cls, name, bases, local):
        print(bases)
        print(local)
        for attr in local:
            value = local[attr]
            if not len(bases) and callable(value) and attr != '__init__':
                local[attr] = Fail_Dealer()(value)
        return super().__new__(cls, name, bases, local) '''


class Fail_Dealer():

    p = SingleTone_local()

    def __init__(self):
        ident = threading.get_ident()
        self.l = self.p._variable[ident]
        self.ERROR = Error_Code()
         

    def get_runtime(self):
        runtime = str(time.time() - self.l['_test_item_start_timer'])
        runtime = int(runtime.split('.')[0])
        return runtime
    
    def sys_exception(self, ex):
        #只有這三種錯誤式系統的exception，所以直接在UI彈出提示視窗   
        if 'FileNotFoundError' in str(ex):           #console連接錯誤 電腦找不到這個port口
            self.l['_sys_error_msg'].append('Comport 找不到指定port口')
                
        elif 'PermissionError' in str(ex):             #console連接錯誤 port口被其他程式使
            self.l['_sys_error_msg'].append('Comport Port口被占据')
        
        elif 'WinError 10061' in str(ex):                    #telnet連接錯誤 telnet被占線
            self.l['_sys_error_msg'].append('Telnet连线被占据')

        else:
            error_msg = exceptions.error_dealer(ex)
            print(error_msg)
            self.l['_sys_error_msg'].append(error_msg)
    
    
    def deal_result(self, result, test_name):
        if result:   
            self.l['_upload_data'][test_name] = (1, None, None, None, None, self.get_runtime())
        else:       #timeout fail
            self.l['dut_been_test_fail'] = True
            self.l['_dut_test_fail'] = True
            self.l['_dut_error_code'] = self.ERROR[test_name]
            error_msg = f"[{test_name}] time out"
            self.l['_test_error_msg'] += error_msg
            self.l['_debug_logger'].debug(f"{error_msg:*^100}")
            self.l['_upload_data'][test_name] = (0, None, None, None, self.ERROR[test_name], self.get_runtime())

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                test_name = sys._getframe(1).f_code.co_name
                
                result, data = func(*args, **kwargs)

                self.l['_log_raw_data'][test_name]['log'] += data
                self.l['_tmp_log'] = data
                self.deal_result(result, test_name)
                if not result:   
                    raise TimeOutError

            except Exception as ex:
                print(ex)
                """連上錯誤"""
                self.l['_log_raw_data'][test_name]['log'] += ''
                self.l['_upload_data'][test_name] = (0, None, None, None, self.ERROR[test_name], self.get_runtime())
                self.sys_exception(ex)
                raise Exception 

            else:
                return True
        return decorated


class COM():

    def __init__(self, port, baud, debug_logger, **awags):
        self.debug_logger = debug_logger
        self.port = port
        self.baud = int(baud)
        self.bytesize = 8 if not awags.get('bytesize') else awags.get('bytesize')
        self.stopbits = 1 if not awags.get('stopbits') else awags.get('stopbits')
        self.parity = 'N' if not awags.get('parity') else awags.get('parity')
        self.com = None
        self.ports_list = []

    @Fail_Dealer()
    def check_connect(self):
        self.close_telnet()
        with serial.Serial(port = self.port, baudrate = self.baud, bytesize=self.bytesize, parity = self.parity, timeout=1, stopbits=self.stopbits) as self.com:
            time.sleep(0.1)
            buffer = self.com.read(self.com.inWaiting())
            #print('buffer:', buffer)   
        self.close_telnet()
        return True, ''
    
    def close_telnet(self):
        if self.com is not None and self.com.isOpen:
            self.com.close()
        
    
    def open_com(self):
        if self.com is not None and self.com.isOpen:
            buffer = self.com.read(self.com.inWaiting())
            print('buffer:', buffer)
            self.com.close()
        self.com = serial.Serial(port = self.port, baudrate = self.baud, bytesize=self.bytesize, parity = self.parity, timeout=1, stopbits=self.stopbits)
        time.sleep(0.1)
        buffer = self.com.read(self.com.inWaiting())
        print('buffer:', buffer)

    @staticmethod
    def to_bytes(command):
        return f"{command}\r\n".encode("utf-8")

    @Fail_Dealer()
    def send_and_receive(self, command, goal_word, timeout, *goal_array:tuple):
        """
        參數(指令、目標字、timout, *goal_array(多個目標))
        goal_array 填參數方式(command, goal_word, timeout, goal_2, goal_3, goal_4...)
        如果goal_array只有一個，請再最後加',' (command, goal_word, timeout, goal_2,)
        exception為:系統找不到port口、port口被占用、timout三種
        """
        Tmp_data = str()
        with serial.Serial(port = self.port, baudrate = self.baud, bytesize=self.bytesize, parity = self.parity, timeout=1, stopbits=self.stopbits) as self.com:
            time.sleep(0.1)
            buffer = self.com.read(self.com.inWaiting())
            #print('buffer:', buffer)
            start_time = time.time()

            if command != None:
                self.debug_logger.debug(f"port [{self.port}] COMMAND: {command}")
                self.com.write(self.to_bytes(command))
            if goal_word != None:
                while True :
                    end_time = time.time()
                    data = self.com.readline().decode("utf-8", errors="backslashreplace")
                    if end_time - start_time > timeout:
                        self.debug_logger.debug(f"port [{self.port}] timeout! log:{Tmp_data}")

                        buffer = self.com.read(self.com.inWaiting())
                        #print('buffer:', buffer)
                        return False, Tmp_data
                    
                    else:
                        if data != '':
                            Tmp_data += data
                            print(data, end = '')
                            self.debug_logger.debug(f"port [{self.port}] RECEIVE : {data.strip()}")
                            if len(goal_array):       #如果有多個目標
                                for word in goal_array:
                                    if (goal_word in data.strip()) or (word in data.strip()):
                                        
                                        buffer = self.com.read(self.com.inWaiting())
                                        #print('buffer:', buffer)
                                        time.sleep(0.1)
                                        return True, Tmp_data
                                    
                            else:
                                if goal_word in data.strip():
                        
                                    buffer = self.com.read(self.com.inWaiting())
                                    #print('buffer:', buffer)
                                    time.sleep(0.1)
                                    return True, Tmp_data
                                      
class Telnet():
    def __init__(self, host, port, debug_logger):
        self.debug_logger = debug_logger
        self.host = str(host)
        self.port = port
        self.tn = None 
    
    @staticmethod
    def to_bytes(command):
        return f"{command}\r\n".encode("utf-8")
    
    @Fail_Dealer()
    def check_connect(self):
        """
        確認telnet是否連線
        """
        self.close_telnet()
        with telnetlib.Telnet(host=self.host, port=self.port) as self.tn:
            time.sleep(0.1)
            buffer = self.tn.read_very_eager()
            #print('buffer', buffer)
        self.close_telnet()
        return True, ''

        
    def open_telnet(self):
        if self.tn is not None:
            buffer = self.tn.read_very_eager()
            self.tn.close()
        self.tn = telnetlib.Telnet(host=self.host, port=self.port, timeout=1)
        time.sleep(0.1)             #需要休息一段時間，不然會送不出去(來不及連接就送指令)
        buffer = self.tn.read_very_eager()
    
    def close_telnet(self):
        if self.tn is not None:
            self.tn.close()
            self.debug_logger.debug(f"port [{self.port}] close port")
        else:
            self.debug_logger.debug(f"port [{self.port}] self.tn is none")
        
    
    '''def send_and_receive(self, command, goal_word, timeout, *goal_array:tuple):
        """
        送指令跟收特定的字，收字必須一定要使用最後一個字，不然DUT可能會收到奇怪的指令而壞掉
        參數(指令、目標字、timout, *goal_array(多個目標))
        goal_array 填參數方式(command, goal_word, timeout, goal_2, goal_3, goal_4...)
        如果goal_array只有一個，請在最後加',' (command, goal_word, timeout, goal_2,)
        exception為:系統找不到port口、port口被占用、timout三種
        """

        with telnetlib.Telnet(host=self.host, port=self.port) as self.tn:
            time.sleep(0.1) 
            buffer = self.tn.read_very_eager()
            print("buffer:", buffer)
            self.Tmp_data = ''
            if command != None:
                time.sleep(0.1)                     #需要休息一段時間，不然會送不出去(來不及連接就送指令)                                      
                self.tn.write(self.to_bytes(command))

            if goal_word != None:
                start_time = time.time()
                while True:
                    end_time = time.time()
                    data_row = self.tn.read_until('\r\n'.encode(), 0.5)
                    data = data_row.decode("utf-8", errors="backslashreplace")
                
                    if end_time - start_time > timeout:
                        time.sleep(0.1)                     #必須休息一小段時間
                        print(self.Tmp_data)
                        buffer = self.tn.read_very_eager()
                        print("buffer:", buffer)
                        self.exception = f'Recive String Timeout=={self.Tmp_data}'
                        raise TimeOutError(self.exception)
                            
                    else:
                        if data != '':
                            self.Tmp_data += data
                            print(data, end = '')
                            data_strip = data.strip()
                            if len(goal_array) != 0:            #如果有第二個目標
                                for word in goal_array:
                                    if (goal_word in data_strip) or (word in data_strip):
                                        time.sleep(0.1)     
                                        buffer = self.tn.read_very_eager()
                                        print("buffer:", buffer)
                                        return self.Tmp_data
                                    
                            else:
                                if goal_word in data_strip:
                                    time.sleep(0.1)
                                    buffer = self.tn.read_very_eager()
                                    print("buffer:", buffer)
                                    break
                                            
                return self.Tmp_data'''

    @Fail_Dealer()
    def send_and_receive(self, command, goal_word, timeout, *goal_array:tuple):
        """
        送指令跟收特定的字，收字必須一定要使用最後一個字，不然DUT可能會收到奇怪的指令而壞掉
        參數(指令、目標字、timout, *goal_array(多個目標))
        goal_array 填參數方式(command, goal_word, timeout, goal_2, goal_3, goal_4...)
        如果goal_array只有一個，請再最後加',' (command, goal_word, timeout, goal_2,)
        exception為:系統找不到port口、port口被占用、timout三種
        """
        Tmp_data = str()
        with telnetlib.Telnet(host=self.host, port=self.port) as self.tn:
            buffer = self.tn.read_very_eager()
            if command != None: 
                time.sleep(0.1) 
                self.debug_logger.debug(f"port [{self.port}] COMMAND: {command}")                            
                self.tn.write(self.to_bytes())
                
            if goal_word != None:
                start_time = time.time()
                while True:
                    time.sleep(0.1)
                    end_time = time.time()
                    data_row = self.tn.read_until('\r\n'.encode(), 0.5)
                    data = data_row.decode("utf-8", errors="backslashreplace")
                
                    if end_time - start_time > timeout:
                        time.sleep(0.1)                     #必須休息一小段時間
                        self.debug_logger.debug(f"port [{self.port}] timeout! log:{Tmp_data}")
                        buffer = self.tn.read_very_eager()
                        self.Variable.raw_log = {'log': Tmp_data}
                        return False, Tmp_data
                            
                    else:
                        if data != '':
                            Tmp_data += data
                            print(data, end = '')
                            self.debug_logger.debug(f"port [{self.port}] RECEIVE : {data.strip()}")
                            if len(goal_array) != 0:
                                for word in goal_array:
                                    if (goal_word in data.strip()) or (word in data.strip()):     
                                        buffer = self.tn.read_very_eager()
                                        #print('buffer:', buffer)
                                        time.sleep(0.1)
                                        return True, Tmp_data           
                                    
                            else:
                                if goal_word in data.strip():
                                    buffer = self.tn.read_very_eager()
                                    #print('buffer:', buffer)
                                    time.sleep(0.1)
                                    return True, Tmp_data    
                                     


        


if __name__ == "__main__":
    
    com = COM('COM4', 9600)
    com.close_com()
    com.open_com()
    com.close_com()
    

    

