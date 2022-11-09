from datetime import datetime
from FTP import FTP_UP_Down
from SFIS import SFIS
import time
from concurrent.futures import ThreadPoolExecutor
from exceptions import Online_Fail, CheckRoute_Fail


class Upload_FTP():

    def __init__(self, ftp_upload_path, Variable):
        self.Variable = Variable
        self.debug_logger = self.Variable.upload_debug_logger
        self.ftp = FTP_UP_Down(self.debug_logger)
        self.ftp_upload_path = ftp_upload_path
        self.ip = '172.24.255.118'
        self.port = 2100
        self.user = 'logbackup'
        self.password = 'pega#$34'

    def ftb_upload_file(self, file_path, remotedir):
        try:
            self.ftp.connect_ftp(self.ip, self.port, self.user, self.password)
            self.ftp.UploadFile(file_path, remotedir)
            self.ftp.close()
        except Exception as ex:
            self.Variable.ftp_error_msg += str(ex)
            raise Online_Fail

    

class SFIS_Function():

    def __init__(self, op, Variable):
        self.Variable = Variable
        self.SFIS_logger = self.Variable.upload_debug_logger
        self.sfis=SFIS() 
        self.deviceID = self.Variable.device_id
        self.sfis_op = op
        self.TSP = 'Burnin'


    def sfis_login(self):
        sfis_data = self.sfis.Logout(self.sfis_op, self.deviceID, self.TSP)
        self.SFIS_logger.debug(f'[SFIS check route] logout: {sfis_data}')
        sfis_data = self.sfis.Login(self.sfis_op, self.deviceID, self.TSP)
        self.SFIS_logger.debug(f'[SFIS check route] login: {sfis_data}')
        
    def sfis_checkroute(self, SSN):
        self.Variable.raw_log['sfis_checkroute'] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        test_start_time = time.time()
        
        self.sfis_login()
        self.SFIS_logger.debug(f'[SFIS check route] get SSN: {SSN} ,deviceID: {self.deviceID}')
        retry_times = 0
        while True:
            sfis_data = self.sfis.CheckRoute(SSN, self.deviceID)
            self.SFIS_logger.debug(f'[SFIS check route] chekroute: {sfis_data}')
            if sfis_data:
                if int(sfis_data[0]) == 1:
                    self.SFIS_logger.debug(f'[SFIS check route] chekroute >>PASS<<')

                    self.Variable.upload_log['sfis_checkroute'] = (1, None, None, None, None, time.time()-test_start_time)
                    self.Variable.raw_log['sfis_checkroute']['log'] = ','.join(sfis_data)
                    self.Variable.raw_log['sfis_checkroute']['end_time'] = datetime.now()
                    return 0
                else:
                    self.Variable.upload_log['sfis_checkroute'] = (0, None, None, None, None, time.time()-test_start_time)
                    self.Variable.raw_log['sfis_checkroute']['log'] = ','.join(sfis_data)
                    self.Variable.raw_log['sfis_checkroute']['end_time'] = datetime.now()


                    if "WRONG STEP" in sfis_data[1]:
                        sfis_error_msg = f'進錯站: {sfis_data[1]}'
                        self.SFIS_logger.debug(f'[SFIS check route] chekroute >>WRONG STEP<< : {sfis_data[1]}')
                        if retry_times < 1:
                            retry_times += 1
                            self.SFIS_logger.debug(f'[SFIS check route] chekroute retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg += sfis_error_msg
                            self.Variable.sfis_upload_fail = True
                            raise CheckRoute_Fail
                            #return False
                            

                    elif 'ISN NOT INPUT' in sfis_data[1]:
                        sfis_error_msg = f'ISN未填: {sfis_data[1]}'
                        self.SFIS_logger.debug(f'[SFIS check route] chekroute >>ISN NOT INPUT<< : {sfis_data[1]}')
                        if retry_times < 1:
                            retry_times += 1
                            self.SFIS_logger.debug(f'[SFIS check route] chekroute retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg += sfis_error_msg
                            self.Variable.sfis_upload_fail = True
                            raise CheckRoute_Fail

                    else:
                        sfis_error_msg = f'check route fail: {sfis_data[1]}'
                        self.SFIS_logger.debug(f'[SFIS check route] chekroute >>FAIL<< : {sfis_data[1]}')
                        if retry_times < 1:
                            retry_times += 1
                            self.SFIS_logger.debug(f'[SFIS check route] chekroute retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg += sfis_error_msg
                            self.Variable.sfis_upload_fail = True
                            raise CheckRoute_Fail
            else:
                self.Variable.upload_log['sfis_checkroute'] = (0, None, None, None, None, time.time()-test_start_time)
                self.Variable.raw_log['sfis_checkroute']['log'] = ' '
                self.Variable.raw_log['sfis_checkroute']['end_time'] = datetime.now()


                sfis_error_msg = f'check route fail, sfis_data error: {sfis_data}'
                self.SFIS_logger.debug(f'[SFIS check route] chekroute >>FAIL DATA ERROR<< :{sfis_data}')
                print('check route fail, sfis_data error')
                if retry_times < 1:
                    retry_times += 1
                    self.SFIS_logger.debug(f'[SFIS check route] chekroute retry: {retry_times}')
                    continue
                else:
                    self.Variable.sfis_error_msg += sfis_error_msg
                    self.Variable.sfis_upload_fail = True
                    raise CheckRoute_Fail

    def sfis_get_dut_sn(self, SN):
        self.Variable.raw_log['sfis_get_dut_sn'] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        test_start_time = time.time()

        self.sfis_login()
        self.SFIS_logger.debug(f'[SFIS get sn] ,deviceID: {self.deviceID}')
        retry_times = 0
        while True:
            sfis_data = self.sfis.Get_SSN(SN, self.deviceID)
            self.SFIS_logger.debug(f'[SFIS get sn] get sn: {sfis_data}')
            if sfis_data:
                if int(sfis_data[0]) == 1:
                    self.SFIS_logger.debug(f'[SFIS get sn] get sn >>PASS<<')
                    self.Variable.dut_sfis_sn = sfis_data[2].strip()

                    self.Variable.upload_log['sfis_get_dut_sn'] = (1, None, None, None, None, time.time()-test_start_time)
                    self.Variable.raw_log['sfis_get_dut_sn']['log'] = ','.join(sfis_data)
                    self.Variable.raw_log['sfis_get_dut_sn']['end_time'] = datetime.now()
                    return 0
                else:
                    self.Variable.upload_log['sfis_get_dut_sn'] = (0, None, None, None, None, time.time()-test_start_time)
                    self.Variable.raw_log['sfis_get_dut_sn']['log'] = ','.join(sfis_data)
                    self.Variable.raw_log['sfis_get_dut_sn']['end_time'] = datetime.now()

                    sfis_error_msg = f'sfis get sn fail, sfis_data error: {sfis_data[1]}'
                    self.SFIS_logger.debug(f'[SFIS get sn] get sn >>FAIL<< :{sfis_data[1]}')

                    if retry_times < 1:
                        retry_times += 1
                        self.SFIS_logger.debug(f'[SFIS get sn] get sn retry: {retry_times}')
                        continue
                    else:
                        self.Variable.sfis_error_msg += sfis_error_msg
                        self.Variable.sfis_get_sn_fail = True
                        raise Online_Fail
            
            else:
                self.Variable.upload_log['sfis_get_dut_sn'] = (0, None, None, None, None, time.time()-test_start_time)
                self.Variable.raw_log['sfis_get_dut_sn']['log'] = ' ' 
                self.Variable.raw_log['sfis_get_dut_sn']['end_time'] = datetime.now()


                sfis_error_msg = f'sfis get sn fail, sfis_data error: {sfis_data}'
                self.SFIS_logger.debug(f'[SFIS get sn] get sn >>FAIL DATA ERROR<< :{sfis_data}')

                if retry_times < 1:
                    retry_times += 1
                    self.SFIS_logger.debug(f'[SFIS get sn] get sn retry: {retry_times}')
                    continue
                else:
                    self.Variable.sfis_error_msg += sfis_error_msg
                    self.Variable.sfis_get_sn_fail = True
                    raise Online_Fail




    def sfis_upload(self, SSN, error, sfis_data, status = 1):
        self.Variable.raw_log['sfis_upload'] = {'start_time': datetime.now(), 'log':'', 'end_time':None}
        test_start_time = time.time()

        self.sfis_login()
        
        self.SFIS_logger.debug(f'[SFIS upload] get SSN: {SSN} , error: {error}, deviceID: {self.deviceID}, sfis_data: {sfis_data}')
        retry_times = 0
        data = str()
        data2 = str()
        data3 = str()
        data4 = str()
        data5 = str()
        data6 = str()
        data7 = str()
        data8 = str()

        
        
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
                    self.SFIS_logger.debug(f'[SFIS upload] upload >>PASS<<')

                    self.Variable.upload_log['sfis_upload'] = (1, None, None, None, None, time.time()-test_start_time)
                    self.Variable.raw_log['sfis_upload']['log'] = ','.join(sfis_data)
                    self.Variable.raw_log['sfis_upload']['end_time'] = datetime.now()
                    return 0
                else:
                    self.Variable.upload_log['sfis_upload'] = (0, None, None, None, None, time.time()-test_start_time)
                    self.Variable.raw_log['sfis_upload']['log'] = ','.join(sfis_data)
                    self.Variable.raw_log['sfis_upload']['end_time'] = datetime.now()

                    if "WRONG STEP" in sfis_data[1]:
                        sfis_error_msg = f'進錯站: {sfis_data[1]}'
                        self.SFIS_logger.debug(f'[SFIS upload] upload >>WRONG STEP<< :{sfis_data[1]}')
                        print('進錯站')
                        if retry_times < 1:
                            retry_times += 1
                            self.SFIS_logger.debug(f'[SFIS upload] upload retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg += sfis_error_msg
                            self.Variable.sfis_upload_fail = True
                            raise Online_Fail
                            #return False
                    else:
                        sfis_error_msg = f'SFIS upload failed: {sfis_data[1]}'
                        self.SFIS_logger.debug(f'[SFIS upload] upload >>FAIL<< :{sfis_data[1]}')
                        print(sfis_error_msg)
                        if retry_times < 1:
                            retry_times += 1
                            self.SFIS_logger.debug(f'[SFIS upload] upload retry: {retry_times}')
                            continue
                        else:
                            self.Variable.sfis_error_msg += sfis_error_msg
                            self.Variable.sfis_upload_fail = True
                            raise Online_Fail
                            #return False
            else:
                self.Variable.upload_log['sfis_upload'] = (0, None, None, None, None, time.time()-test_start_time)
                self.Variable.raw_log['sfis_upload']['log'] = ' '
                self.Variable.raw_log['sfis_upload']['end_time'] = datetime.now()



                sfis_error_msg = f'SFIS upload failed, sfis_data error: {sfis_data[1]}'
                self.SFIS_logger.debug(f'[SFIS upload] upload >>FAIL SFIS DATA ERROR<< :{sfis_data[1]}')
                print('SFIS upload failed')
                if retry_times < 1:
                    retry_times += 1
                    self.SFIS_logger.debug(f'[SFIS upload] upload retry: {retry_times}')
                    continue
                else:
                    self.Variable.sfis_error_msg += sfis_error_msg
                    self.Variable.sfis_upload_fail = True
                    raise Online_Fail
                    #return False
    
if "__main__" == __name__:
    ii = SFIS_Function('LA2100645', )
