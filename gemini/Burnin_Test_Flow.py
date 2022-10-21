import time
import os
from copy import deepcopy
import threading
import Burnin_log as Write_log
from functools import wraps
import Burnin_Test_Item as Test_Item
import file_util
import FTP
from concurrent.futures import ThreadPoolExecutor
from SFIS import SFIS
from exceptions import Test_Fail

VERSION = ''

#telnet設定
telnet_ip = "10.1.1.2"
telnet_ports = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 
               2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
open_station = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sfis_deviceID = {2002:'992632', 2003:'992631', 2004:'992630', 2005:'992629', 2006:'992628', 2007:'992627', 2008:'992626', 2009:'992625', 2010:'992624', 2011:'992622',
                2012:'992632', 2013:'992631', 2014:'992630', 2015:'992629', 2016:'992628', 2017:'992627', 2018:'992626', 2019:'992625', 2020:'992624', 2021:'992622'}
    
#logger設定
logger_path = r'.\debug'
test_log_path = r'.\log\test.txt'

value_config_path = r"D:\Qian\python\NPI\Gemini\value_config.ini"

SFIS_logger = file_util.create_logger(logger_path, 'SFIS_log')


#測試參數
signal = None
serial_name = 'EZ1K_A1'
serial_port = '8'
terminal_server_comport = 'COM4'
pg_comport = 'COM5'
package_machine = 'Nustream'
test_time = 48
ftp_upload_funtion = False
ftp_upload_path = '/SWITCH/EZ1K-ORT'
SFIS_function = True
sfis_op = ''

#封包機參數
nustream_initial_tcl_path = r'C:\TCL\bin\DUT1_1000M_10s_card.tcl'
nustream_packaging_tcl_path = r'C:\TCL\bin\DUT1_1000M_480s_card.tcl'   
pg_initial_test_time = 20          #pg在initial裡面的測試時間(s)
pg_packing_test_time = 470         #pg在打封包測試裡面的測試時間(s)
packing_rest_time = 116             #116

#錯誤訊息
UI_msg = dict()


sfis_log_other = str()
dut_SSN_dic = dict()
all_sfis_log = dict()
all_sfis_error_code = dict()
checkroute_data = dict()



#測試完儲存下來的DUT資訊(port : serial name)，會先送到controller，等到打封包測試時再送回來
dut_finish_initial_data = dict()


#region 接入從controller下達的參數
def get_veriable_from_controller(**kwargs):
    global signal

    global VERSION
    global open_station
    global serial_name
    global serial_port
    global terminal_server_comport
    global pg_comport
    global package_machine
    global test_time
    global ftp_upload_funtion
    global ftp_upload_path
    global SFIS_function
    global sfis_op

    global dut_finish_initial_data

    signal = kwargs.get('signal')
    config = kwargs.get('config')
    VERSION = kwargs.get('VERSION')
    if config:
        serial_name = config['serial_name']
        serial_port = str(config['serial_port'])
        terminal_server_comport = config['terminal_server_comport']
        pg_comport = config['pg_comport']
        package_machine = config['package_machine']
        test_time = config['test_time']
        open_station = config['open_station']
        ftp_upload_funtion = config['ftp_upload_funtion']
        ftp_upload_path = config['ftp_upload_path']
        ftp_upload_path = ftp_upload_path.replace('\\', '/').strip('/')
        SFIS_function = config['SFIS_function']
        sfis_op = config['op']
        
    if kwargs.get('dut_data'):
        dut_finish_initial_data = kwargs['dut_data']
    
#endregion

#region 送訊息到UI
def send_to_ui(msg):
    """
    送訊息到UI controller
    """
    if signal:   
        signal.status.emit(msg)
#endregion

class Flow_MetaClass(type):
    def __new__(cls, name, bases, local):
        if len(bases):
            for base in bases:
                if base != Flow:
                    Variable = base.Variable
            local['Variable'] = Variable
            for attr in local:
                value = local[attr]
                if callable(value) and attr != '__init__':
                    local[attr] = Fail_Dealer(Variable)(value)
        return super().__new__(cls, name, bases, local)

class Fail_Dealer():
    def __init__(self, Variable):
        pass
        self.Variable = Variable
        #self.func = func

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                func(*args, **kwargs)

            except Test_Fail:
                print(self.Variable)
                return False
                
            except Exception:
                print(self.Variable.sys_error_msg)
                return False

            else:
                print(self.Variable.log)
                print(self.Variable.upload_log)
                return True
        return decorated



class Flow(metaclass = Flow_MetaClass):
    pass

class mChild(type(Flow), type(Test_Item.Terminal_Server_Test_Item)):
    pass
       
class Terminal_Server(Flow, Test_Item.Terminal_Server_Test_Item, metaclass = mChild):

    def __init__(self, terminal_comport):
        self.baud = '9600'
        self.terminal_comport = terminal_comport
        self.logger = file_util.create_logger(logger_path, 'main_log')
        super().__init__(port = self.terminal_comport, baud = self.baud, logger = self.logger)  

    def Check_All_Comport(self):
        """
        確認terminal server和pg的port口是否正常
        """
        self.Check_Comport()
    
    def Terminal_Server_Flow(self):
        """
        terminal server清線
        """
        self.Enter_en_Mode()
        self.Clear_Port_on_Terminal(2, 23)


class mChild(type(Flow), type(Test_Item.Gemini_Test_Item)):
    pass 

class Gemini(Flow, Test_Item.Gemini_Test_Item, metaclass = mChild):

    def __init__(self, telnet_port):
        self.telnet_port = telnet_port
        self.Gemini_logger = file_util.create_logger(logger_path, f"Gemini {telnet_port}_log")
        super().__init__(ip = telnet_ip, port = self.telnet_port, logger = self.Gemini_logger, value_config_path = value_config_path)  

    def Gemini_Test_Flow(self):
        """
        Gemini測試流程
        """
        self.Gemini_logger.debug(f"port [{self.telnet_port}] in [Gemini_Test_Flow]")
        self.Check_Telnet_Connect()
        self.Boot_Up()
        self.Set_Two_Power()
        self.Check_HW_SW_Ver()
        self.Check_RTC()    
        self.Check_HW_Monitor()
        self.Check_Fan0_Speed()
        self.Check_Fan100_Speed()
        self.DRAM_Test()
        self.SSD_Test()
        self.Module_Signal_Check()
        self.Set_Loopback_3_5W()
        self.Traffic_Test()
        self.Loopbak_Test()

        with open(test_log_path, 'w') as f:
            f.write(self.Variable.log)
        print(self.Variable.upload_log)
        









def start_upload_ftb_thread(upload_file_list):
    ftp_path_list = list()
    error_msg = ''
    upload_flag = True
    ui_msg = dict()
    future_list = list()

    for path in upload_file_list:  #upload_file_list:[(dut_port, log_path, ftp_path)]
        ftp_path = f"/{ftp_upload_path}/{path[2]}"
        print('ftp_path:', ftp_path)
        ftp_path_list.append(ftp_path)

    with ThreadPoolExecutor(max_workers=len(upload_file_list)) as executor:
        for i, ftp_path in enumerate(ftp_path_list):
            futures = executor.submit(ftb_upload_file_flow, upload_file_list[i][1], ftp_path)
            future_list.append(futures)
            time.sleep(0.1)

    for future in future_list:
        exception = future.exception()
        if exception:
            #main_logger.exception(f"Upload FTP exception {exception}")
            error_msg += f"{upload_file_list[i][0]}\n"
            upload_flag = False
        else:
            main_logger.info(f'upload {upload_file_list[i][0]} success')

    if not upload_flag:
        error_msg += f"exception: {exception}"
        ui_msg['messagebox_2'] = ['Upload FTP error', error_msg]
        send_to_ui(ui_msg)  
    return 0
        

def ftb_upload_file_flow(file_path, remotedir):
    ip = '172.24.255.118'
    port = 2100
    user = 'logbackup'
    password = 'pega#$34' #pega#$34
    f = FTP.FTP_UP_Down()
    f.connect_ftp(ip, port, user, password)
    f.UploadFile(file_path, remotedir)
    f.close()

def sfis_checkroute_thread():
    global dut_SSN_dic 
    global sfis_deviceID
    global checkroute_data
    global UI_msg

    UI_msg.clear()
    ui_msgggg = dict()
    future_dict = dict()
    umsg = ''
    SFIS_logger.debug(f'[SFIS check route] get dut_SSN_dic:{dut_SSN_dic}')
    with ThreadPoolExecutor(max_workers=len(dut_SSN_dic)) as executor:
        for port, dut_ssn in dut_SSN_dic.items():
            futures = executor.submit(sfis_checkroute_flow, dut_ssn, sfis_deviceID[port])
            future_dict[port] = futures
    

    for port, future in future_dict.items():
        exception = future.exception()
        if not exception:
            msg = future.result()
            if msg:
                umsg += f"DUT {port-2002+1}: {msg}\n"
                UI_msg['single_status_change'] = [port-2002, 'FAIL']
                send_to_ui(UI_msg)
                print(f"DUT {port-2002+1} : {msg}") 
            else:
                print(f"DUT {port-2002+1} checkroute pass")
        else:
            UI_msg['single_status_change'] = [port-2002, 'FAIL']
            send_to_ui(UI_msg)
            umsg += f"DUT {port-2002+1} EXCEPTION: {exception}\n"
            print(f"DUT {port-2002+1} EXCEPTION: {exception}")
        time.sleep(0.1)

    
    if umsg != '':
        SFIS_logger.debug(f'[SFIS check route] get error, {umsg}')
        ui_msgggg['messagebox'] = ['sfis check route error', umsg]
        send_to_ui(ui_msgggg)
        return False    
    return True
    
def sfis_checkroute_flow(SSN, deviceID):
    SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] get SSN: {SSN} ,deviceID: {deviceID}')
    TSP = 'ORT'
    retry_times = 0
    sfis=SFIS()
    sfis_data = sfis.Logout(sfis_op, deviceID, TSP)
    SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] logout: {sfis_data}')
    sfis_data = sfis.Login(sfis_op, deviceID, TSP)
    SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] login: {sfis_data}')
    while True:
        sfis_data = sfis.CheckRoute(SSN, deviceID)
        SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute: {sfis_data}')
        if sfis_data:
            if int(sfis_data[0]) == 1:
                SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>PASS<<')
                return 0
            else:
                if "WRONG STEP" in sfis_data[1]:
                    sfis_error_msg = f'進錯站: {sfis_data[1]}'
                    SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>WRONG STEP<< : {sfis_data[1]}')
                    if retry_times < 1:
                        retry_times += 1
                        SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg

                elif 'ISN NOT INPUT' in sfis_data[1]:
                    sfis_error_msg = f'ISN未填: {sfis_data[1]}'
                    SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>ISN NOT INPUT<< : {sfis_data[1]}')
                    if retry_times < 1:
                        retry_times += 1
                        SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg

                else:
                    sfis_error_msg = f'check route fail: {sfis_data[1]}'
                    SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>FAIL<< : {sfis_data[1]}')
                    if retry_times < 1:
                        retry_times += 1
                        SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg    
        else:
            sfis_error_msg = f'check route fail, sfis_data error: {sfis_data[1]}'
            SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>FAIL DATA ERROR<< :{sfis_data[1]}')
            print('check route fail, sfis_data error')
            if retry_times < 1:
                retry_times += 1
                SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute retry: {retry_times}')
                continue
            else:
                return sfis_error_msg

def sfis_upload_thread():
    global dut_SSN_dic 
    global all_sfis_log 
    global all_sfis_error_code
    global sfis_deviceID
    global checkroute_data
    global UI_msg

    UI_msg.clear()
    ui_msg = dict()
    umsg = ''
    future_dict = dict()
    SFIS_logger.debug(f'[SFIS upload] get all_sfis_error_code: {all_sfis_error_code}, sfis_deviceID: {sfis_deviceID}, all_sfis_log: {all_sfis_log}')
    with ThreadPoolExecutor(max_workers=len(dut_SSN_dic)) as executor:
        for port, dut_ssn in dut_SSN_dic.items():
            futures = executor.submit(sfis_upload_flow, dut_ssn, all_sfis_error_code[port], sfis_deviceID[port], all_sfis_log[port])
            future_dict[port] = futures
           
    

    for port, future in future_dict.items():
        exception = future.exception()
        if not exception:
            msg = future.result()
            if msg:
                print(f"DUT {port-2002+1} : {msg}")
                UI_msg['single_status_change'] = [port-2002, 'FAIL']
                send_to_ui(UI_msg)
                umsg += f"DUT {port-2002+1}: {msg}\n"
            else:
                print(f"DUT {port-2002+1} checkroute pass")

        else:
            UI_msg['single_status_change'] = [port-2002, 'FAIL']
            send_to_ui(UI_msg)
            umsg += f"DUT {port-2002+1} EXCEPTION: {exception}\n"
            print(f"DUT {port-2002+1} EXCEPTION: {exception}")

        time.sleep(0.1)
    
    if umsg != '':
        ui_msg.clear()
        SFIS_logger.debug(f'[SFIS upload] get upload error, {umsg}')
        ui_msg['messagebox'] = ['sfis upload error', umsg]
        send_to_ui(ui_msg)
        return False
    return True


def sfis_upload_flow(SSN, error, deviceID, sfis_data, status = 1):
    SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] get SSN: {SSN} , error: {error}, deviceID: {deviceID}, sfis_data: {sfis_data}')
    TSP = 'ORT'
    retry_times = 0
    data = str()
    data2 = str()
    data3 = str()
    data4 = str()
    data5 = str()
    data6 = str()
    data7 = str()
    data8 = str()

    sfis=SFIS()
    sfis.Logout(sfis_op, deviceID, TSP)
    sfis.Login(sfis_op, deviceID, TSP)
    
    data_list = [data,data2,data3,data4,data5,data6,data7,data8]
    
    data_list_index = 0
    while True:
        data_list[data_list_index] = sfis_data
        if len(sfis_data) > 31000:
            tmp_data = sfis_data[:31000]
            tmp_index = tmp_data.rfind('\r\n')
            tmp_data = tmp_data[:tmp_index]
            data_list[data_list_index] = tmp_data
            sfis_data = sfis_data[tmp_index + len('\r\n'): ]
            data_list_index += 1
        else:
            break
    
    while True:
        sfis_data = sfis.UploadRawData(SSN, error, deviceID, TSP, status, data_list)
        if sfis_data:
            if int(sfis_data[0]) == 1:
                SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload >>PASS<<')
                print('SFIS upload success')
                return 0
            else:
                if "WRONG STEP" in sfis_data[1]:
                    sfis_error_msg = f'進錯站: {sfis_data[1]}'
                    SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload >>WRONG STEP<< :{sfis_data[1]}')
                    print('進錯站')
                    if retry_times < 1:
                        retry_times += 1
                        SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg  
                else:
                    sfis_error_msg = f'SFIS upload failed: {sfis_data[1]}'
                    SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload >>FAIL<< :{sfis_data[1]}')
                    print(sfis_error_msg)
                    if retry_times < 1:
                        retry_times += 1
                        SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg  
        else:
            sfis_error_msg = f'SFIS upload failed, sfis_data error: {sfis_data[1]}'
            SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload >>FAIL SFIS DATA ERROR<< :{sfis_data[1]}')
            print('SFIS upload failed')
            if retry_times < 1:
                retry_times += 1
                SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload retry: {retry_times}')
                continue
            else:
                return sfis_error_msg

if "__main__" == __name__:
    terminal_server_comport = 'COM7'
    telnet_port = 2002
    telnet_ip = "10.1.1.2"
    te = Terminal_Server(terminal_server_comport)
    #print(Terminal_Server.__dict__)
    te.Terminal_Server_Flow()
    #Gemini_Test_Flow(telnet_port)
    #Start_DUT_Initial()
    #Packaging_Loop()
    #Check_All_Comport()
    #DUT_Get_Counter_Thread() 