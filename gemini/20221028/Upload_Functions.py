import time
from FTP import FTP_UP_Down
from SFIS import SFIS
from concurrent.futures import ThreadPoolExecutor
from exceptions import Online_Fail

logger_path = r'.\debug'


class Upload_FTP():

    def __init__(self, ftp_upload_path, Variable, thread_global, logger):
        self.Variable = Variable
        self.thread_global = thread_global
        self.debug_logger = logger
        self.ftp = FTP_UP_Down(self.debug_logger)
        self.ftp_upload_path = ftp_upload_path
        self.ip = '172.24.255.118'
        self.port = 2100
        self.user = 'logbackup'
        self.password = 'pega#$34'


    ''' def start_upload_ftb_thread(self,upload_file_list):
        ftp_path_list = list()
        error_msg = ''
        ui_msg = dict()
        future_list = list()

        for path in upload_file_list:  #upload_file_list:[(dut_port, log_path, ftp_path)]
            ftp_path = f"/{self.ftp_upload_path}/{path[2]}"
            print('ftp_path:', ftp_path)
            ftp_path_list.append(ftp_path)

        with ThreadPoolExecutor(max_workers=len(upload_file_list)) as executor:
            for i, ftp_path in enumerate(ftp_path_list):
                futures = executor.submit(self.ftb_upload_file, upload_file_list[i][1], ftp_path)
                future_list.append(futures)
                time.sleep(0.1)

        for future in future_list:
            exception = future.exception()
            if exception:
                self.FTP_logger.exception(f"Upload FTP exception {exception}")
                error_msg += f"{upload_file_list[i][0]}\n"
                upload_flag = False
            else:
                self.FTP_logger.info(f'upload {upload_file_list[i][0]} success')

        if not upload_flag:
            error_msg += f"exception: {exception}"
            ui_msg['messagebox_2'] = ['Upload FTP error', error_msg]
             
        return 0 '''


    def ftb_upload_file(self, file_path, remotedir):
        try:
            self.ftp.connect_ftp(self.ip, self.port, self.user, self.password)
            self.ftp.UploadFile(file_path, remotedir)
            self.ftp.close()
        except Exception as ex:
            self.Variable.ftp_error_msg = str(ex)
            raise Online_Fail
            #return False

    

class SFIS_Function():

    def __init__(self, threal_local, thread_global ,GLOBAL, logger):
        self.threal_local = threal_local
        self.thread_global = thread_global
        self.GLOBAL = GLOBAL
        self.SFIS_logger = logger
        self.sfis=SFIS() 
        self.deviceID = self.thread_global.device_ID
        self.sfis_op = self.GLOBAL.op
        self.TSP = 'Burnin'
            

    ''' def SFIS_Checkroute_Thread(self):
        ui_msgggg = dict()
        future_dict = dict()
        umsg = ''
        self.SFIS_logger.debug(f'[SFIS check route] get dut_SSN_dic:{dut_SSN_dic}')

        with ThreadPoolExecutor(max_workers=len(dut_SSN_dic)) as executor:
            for port, dut_ssn in dut_SSN_dic.items():
                futures = executor.submit(self.sfis_checkroute, dut_ssn, self.deviceID[port])
                future_dict[port] = futures
        
        for port, future in future_dict.items():
            exception = future.exception()
            if not exception:
                msg = future.result()
                if msg:
                    umsg += f"DUT {port-2002+1}: {msg}\n"
                    UI_msg['single_status_change'] = [port-2002, 'FAIL']
                    
                    print(f"DUT {port-2002+1} : {msg}") 
                else:
                    print(f"DUT {port-2002+1} checkroute pass")
            else:
                UI_msg['single_status_change'] = [port-2002, 'FAIL']
                
                umsg += f"DUT {port-2002+1} EXCEPTION: {exception}\n"
                print(f"DUT {port-2002+1} EXCEPTION: {exception}")
            time.sleep(0.1)

        
        if umsg != '':
            self.SFIS_logger.debug(f'[SFIS check route] get error, {umsg}')
            ui_msgggg['messagebox'] = ['sfis check route error', umsg]
            
            return False    
        return True
 '''
        
    def sfis_checkroute(self, SSN):
        #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] get SSN: {SSN} ,deviceID: {self.deviceID}')
        
        retry_times = 0
        
        sfis_data = self.sfis.Logout(self.sfis_op, self.deviceID, self.TSP)
        #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] logout: {sfis_data}')
        sfis_data = self.sfis.Login(self.sfis_op, self.deviceID, self.TSP)
        #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] login: {sfis_data}')
        while True:
            sfis_data = self.sfis.CheckRoute(SSN, self.deviceID)
            #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute: {sfis_data}')
            if sfis_data:
                if int(sfis_data[0]) == 1:
                    #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute >>PASS<<')
                    return 0
                else:
                    if "WRONG STEP" in sfis_data[1]:
                        sfis_error_msg = f'進錯站: {sfis_data[1]}'
                        #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute >>WRONG STEP<< : {sfis_data[1]}')
                        if retry_times < 1:
                            retry_times += 1
                            #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg = sfis_error_msg
                            self.Variable.check_route_fail = True
                            raise Online_Fail
                            #return False
                            

                    elif 'ISN NOT INPUT' in sfis_data[1]:
                        sfis_error_msg = f'ISN未填: {sfis_data[1]}'
                        #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute >>ISN NOT INPUT<< : {sfis_data[1]}')
                        if retry_times < 1:
                            retry_times += 1
                            #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg = sfis_error_msg
                            self.Variable.check_route_fail = True
                            raise Online_Fail

                    else:
                        sfis_error_msg = f'check route fail: {sfis_data[1]}'
                        #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute >>FAIL<< : {sfis_data[1]}')
                        if retry_times < 1:
                            retry_times += 1
                            #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg = sfis_error_msg
                            self.Variable.check_route_fail = True
                            raise Online_Fail 
            else:
                sfis_error_msg = f'check route fail, sfis_data error: {sfis_data[1]}'
                #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute >>FAIL DATA ERROR<< :{sfis_data[1]}')
                print('check route fail, sfis_data error')
                if retry_times < 1:
                    retry_times += 1
                    #self.SFIS_logger.debug(f'[SFIS check route] in [{self.deviceID}] chekroute retry: {retry_times}')
                    continue
                else:
                    self.Variable.sfis_error_msg = sfis_error_msg
                    self.Variable.check_route_fail = True
                    raise Online_Fail

    ''' def SFIS_Upload_Thread(self):
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
        self.SFIS_logger.debug(f'[SFIS upload] get all_sfis_error_code: {all_sfis_error_code}, sfis_deviceID: {sfis_deviceID}, all_sfis_log: {all_sfis_log}')
        with ThreadPoolExecutor(max_workers=len(dut_SSN_dic)) as executor:
            for port, dut_ssn in dut_SSN_dic.items():
                futures = executor.submit(self.sfis_upload, dut_ssn, all_sfis_error_code[port], sfis_deviceID[port], all_sfis_log[port])
                future_dict[port] = futures
            
        

        for port, future in future_dict.items():
            exception = future.exception()
            if not exception:
                msg = future.result()
                if msg:
                    print(f"DUT {port-2002+1} : {msg}")
                    UI_msg['single_status_change'] = [port-2002, 'FAIL']
                    umsg += f"DUT {port-2002+1}: {msg}\n"
                else:
                    print(f"DUT {port-2002+1} checkroute pass")

            else:
                UI_msg['single_status_change'] = [port-2002, 'FAIL']
                
                umsg += f"DUT {port-2002+1} EXCEPTION: {exception}\n"
                print(f"DUT {port-2002+1} EXCEPTION: {exception}")

            time.sleep(0.1)
        
        if umsg != '':
            ui_msg.clear()
            self.SFIS_logger.debug(f'[SFIS upload] get upload error, {umsg}')
            ui_msg['messagebox'] = ['sfis upload error', umsg]
            
            return False
        return True '''


    def sfis_upload(self, SSN, error, sfis_data, status = 1):
        self.SFIS_logger.debug(f'[SFIS upload] in [{self.deviceID}] get SSN: {SSN} , error: {error}, deviceID: {deviceID}, sfis_data: {sfis_data}')
        retry_times = 0
        data = str()
        data2 = str()
        data3 = str()
        data4 = str()
        data5 = str()
        data6 = str()
        data7 = str()
        data8 = str()

        self.sfis.Logout(self.sfis_op, self.deviceID, self.TSP)
        self.sfis.Login(self.sfis_op, self.deviceID, self.TSP)
        
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
            sfis_data = self.sfis.UploadRawData(SSN, error, self.deviceID, self.TSP, status, data_list)
            if sfis_data:
                if int(sfis_data[0]) == 1:
                    self.SFIS_logger.debug(f'[SFIS upload] in [{self.deviceID}] upload >>PASS<<')
                    print('SFIS upload success')
                    return 0
                else:
                    if "WRONG STEP" in sfis_data[1]:
                        sfis_error_msg = f'進錯站: {sfis_data[1]}'
                        self.SFIS_logger.debug(f'[SFIS upload] in [{self.deviceID}] upload >>WRONG STEP<< :{sfis_data[1]}')
                        print('進錯站')
                        if retry_times < 1:
                            retry_times += 1
                            self.SFIS_logger.debug(f'[SFIS upload] in [{self.deviceID}] upload retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg = sfis_error_msg
                            self.Variable.sfis_upload_fail = True
                            raise Online_Fail
                            #return False
                    else:
                        sfis_error_msg = f'SFIS upload failed: {sfis_data[1]}'
                        self.SFIS_logger.debug(f'[SFIS upload] in [{self.deviceID}] upload >>FAIL<< :{sfis_data[1]}')
                        print(sfis_error_msg)
                        if retry_times < 1:
                            retry_times += 1
                            self.SFIS_logger.debug(f'[SFIS upload] in [{self.deviceID}] upload retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg = sfis_error_msg
                            self.Variable.sfis_upload_fail = True
                            raise Online_Fail
                            #return False
            else:
                sfis_error_msg = f'SFIS upload failed, sfis_data error: {sfis_data[1]}'
                self.SFIS_logger.debug(f'[SFIS upload] in [{self.deviceID}] upload >>FAIL SFIS DATA ERROR<< :{sfis_data[1]}')
                print('SFIS upload failed')
                if retry_times < 1:
                    retry_times += 1
                    self.SFIS_logger.debug(f'[SFIS upload] in [{self.deviceID}] upload retry: {retry_times}')
                    continue
                else:
                    self.Variable.sfis_error_msg = sfis_error_msg
                    self.Variable.sfis_upload_fail = True
                    raise Online_Fail
                    #return False
