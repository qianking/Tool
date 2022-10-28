import time
import serial
import telnetlib
from exceptions import TimeOutError

class COM():
    def __init__(self, port, baud, Variable, **awags):
        self.Variable = Variable
        self.port = port
        self.baud = int(baud)
        self.bytesize = 8
        self.stopbits = 1
        self.parity = 'N'
        self.awags = awags
        self.com = None
        self.ports_list = []
        self.get_variable()

    def get_variable(self):
        if len(self.awags):
            if 'bytesize' in self.awags:
                self.bytesize = self.awags['bytesize']
            if 'stopbits' in self.awags:
                self.stopbits = self.awags['stopbits']
            if 'parity' in self.awags:
                self.parity = self.awags['parity']

    def check_connect(self):
        self.close_com()
        with serial.Serial(port = self.port, baudrate = self.baud, bytesize=self.bytesize, parity = self.parity, timeout=1, stopbits=self.stopbits) as self.com:
            time.sleep(0.1)
            buffer = self.com.read(self.com.inWaiting())
            #print('buffer:', buffer)   
        self.close_com()
    
    def close_com(self):
        if self.com is not None and self.com.isOpen:
            self.com.close()
    
    '''def open_com(self):
        if self.com is not None and self.com.isOpen:
            buffer = self.com.read(self.com.inWaiting())
            print('buffer:', buffer)
            self.com.close()
        self.com = serial.Serial(port = self.port, baudrate = self.baud, bytesize=self.bytesize, parity = self.parity, timeout=1, stopbits=self.stopbits)
        time.sleep(0.1)
        buffer = self.com.read(self.com.inWaiting())
        print('buffer:', buffer)'''

    def to_bytes(self, command):
        return f"{command}\r\n".encode("utf-8")

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
                self.Variable.debug_logger.debug(f"port [{self.port}] COMMAND: {command}")
                self.com.write(self.to_bytes(command))
            if goal_word != None:
                while True :
                    end_time = time.time()
                    data = self.com.readline().decode("utf-8", errors="backslashreplace")
                    if end_time - start_time > timeout:
                        self.Variable.debug_logger.debug(f"port [{self.port}] timeout! log:{Tmp_data}")

                        buffer = self.com.read(self.com.inWaiting())
                        #print('buffer:', buffer)
                        self.Variable.raw_log = {'log': Tmp_data}
                        raise TimeOutError
                    
                    else:
                        if data != '':
                            Tmp_data += data
                            print(data, end = '')
                            self.Variable.debug_logger.debug(f"port [{self.port}] RECEIVE : {data.strip()}")
                            if len(goal_array):       #如果有多個目標
                                for word in goal_array:
                                    if (goal_word in data.strip()) or (word in data.strip()):
                                        
                                        buffer = self.com.read(self.com.inWaiting())
                                        #print('buffer:', buffer)
                                        self.Variable.raw_log = {'log': Tmp_data}
                                        time.sleep(0.1)
                                        return 0
                                    
                            else:
                                if goal_word in data.strip():
                        
                                    buffer = self.com.read(self.com.inWaiting())
                                    #print('buffer:', buffer)
                                    self.Variable.raw_log = {'log': Tmp_data}
                                    time.sleep(0.1)
                                    return 0
                                      
class Telnet():
    def __init__(self, host, port, Variable):
        self.Variable = Variable
        self.host = str(host)
        self.port = port
        self.tn = None
       
    def to_bytes(self, command):
        
        return f"{command}\r\n".encode("utf-8")
    
    def check_connect(self):
        """
        確認telnet是否連線
        """
        with telnetlib.Telnet(host=self.host, port=self.port) as self.tn:
            time.sleep(0.1)
            buffer = self.tn.read_very_eager()
            #print('buffer', buffer)
        self.close_telnet()
        
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
            self.Variable.debug_logger.debug(f"port [{self.port}] close port")
        else:
            self.Variable.debug_logger.debug(f"port [{self.port}] self.tn is none")
        
    
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
                self.Variable.debug_logger.debug(f"port [{self.port}] COMMAND: {command}")                            
                self.tn.write(self.to_bytes(command))
                
            if goal_word != None:
                start_time = time.time()
                while True:
                    time.sleep(0.1)
                    end_time = time.time()
                    data_row = self.tn.read_until('\r\n'.encode(), 0.5)
                    data = data_row.decode("utf-8", errors="backslashreplace")
                
                    if end_time - start_time > timeout:
                        time.sleep(0.1)                     #必須休息一小段時間
                        self.Variable.debug_logger.debug(f"port [{self.port}] timeout! log:{Tmp_data}")
                        buffer = self.tn.read_very_eager()
                        self.Variable.raw_log = {'log': Tmp_data}
                        raise TimeoutError
                            
                    else:
                        if data != '':
                            Tmp_data += data
                            print(data, end = '')
                            self.Variable.debug_logger.debug(f"port [{self.port}] RECEIVE : {data.strip()}")
                            if len(goal_array) != 0:
                                for word in goal_array:
                                    if (goal_word in data.strip()) or (word in data.strip()):     
                                        buffer = self.tn.read_very_eager()
                                        #print('buffer:', buffer)
                                        self.Variable.raw_log = {'log': Tmp_data}
                                        time.sleep(0.1)
                                        return 0              
                                    
                            else:
                                if goal_word in data.strip():
                                    buffer = self.tn.read_very_eager()
                                    #print('buffer:', buffer)
                                    self.Variable.raw_log = {'log': Tmp_data}
                                    time.sleep(0.1)
                                    return 0
                                     


        


if __name__ == "__main__":
    
    com = COM('COM4', 9600)
    com.close_com()
    com.open_com()
    com.close_com()
    

    

