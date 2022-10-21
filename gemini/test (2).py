from SFIS import SFIS
from concurrent.futures import ThreadPoolExecutor

sfis_op = 'LA2100645'
sfis_deviceID = {2002:'992632', 2003:'992631', 2004:'992630', 2005:'992629', 2006:'992628', 2007:'992627', 2008:'992626', 2009:'992625', 2010:'992624', 2011:'992622',
                2012:'992632', 2013:'992631', 2014:'992630', 2015:'992629', 2016:'992628', 2017:'992627', 2018:'992626', 2019:'992625', 2020:'992624', 2021:'992622'}

dut_SSN_dic = {2002:'PSZ26381UJS', 2003:'PSZ26381UHB', 2004: 'PSZ26381UFW', 2012:'PSZ26381UE4', 2013:'PSZ263919AX', 2014: 'PSZ26381UKD'}
checkroute_data = dict()

all_sfis_log = {2002:'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,V0.00.20\r\nBootUp_DUT_Boot_Up,1,PASS\r\nBootUp_Press_Enter,1,PASS\r\nBootUp_Enter_No,0,FAIL\r\n',
                2003:'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,V0.00.20\r\nBootUp_DUT_Boot_Up,1,PASS\r\nBootUp_Press_Enter,1,PASS\r\nBootUp_Enter_No,0,FAIL\r\n', 
                2004:'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,V0.00.20\r\nBootUp_DUT_Boot_Up,1,PASS\r\nBootUp_Press_Enter,1,PASS\r\nBootUp_Enter_No,0,FAIL\r\n', 
                2012:'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,V0.00.20\r\nBootUp_DUT_Boot_Up,1,PASS\r\nBootUp_Press_Enter,1,PASS\r\nBootUp_Enter_No,0,FAIL\r\n',
                2013:'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,V0.00.20\r\nBootUp_DUT_Boot_Up,1,PASS\r\nBootUp_Press_Enter,1,PASS\r\nBootUp_Enter_No,0,FAIL\r\n', 
                2014:'TESTITEM,STATUS,VALUE,UCL,LCL\r\nProgram Version,1,V0.00.20\r\nBootUp_DUT_Boot_Up,1,PASS\r\nBootUp_Press_Enter,1,PASS\r\nBootUp_Enter_No,0,FAIL\r\n', }

all_sfis_error_code = {2002:'', 2003:'', 2004:'', 2012:'', 2013:'', 2014:''}

checkroute_data = {2002:True, 2003:True, 2004:True}

def sfis_checkroute_thread():
    global dut_SSN_dic 
    global sfis_deviceID
    global checkroute_data

    ui_msg = dict()
    umsg = ''
    #SFIS_logger.debug(f'[SFIS check route] get dut_SSN_dic:{dut_SSN_dic}')
    with ThreadPoolExecutor(max_workers=len(dut_SSN_dic)) as executor:
        for port, dut_ssn in dut_SSN_dic.items():
            futures = executor.submit(sfis_checkroute_flow, dut_ssn, sfis_deviceID[port])
            msg = futures.result()
            if msg:
                umsg += f"port {port}: {msg}\n"
                print(f"{port} : {msg}")
                if 'ISN未填' in msg:
                    checkroute_data[port] = False
            else:
                print(f"{port} checkroute pass")
                checkroute_data[port] = True

    if umsg != '':
        #SFIS_logger.debug(f'[SFIS check route] get error, {umsg}')
        ui_msg['messagebox'] = ['sfis check route error', umsg]
        return False    
    return True
    
def sfis_checkroute_flow(SSN, deviceID):
    #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] get SSN: {SSN} ,deviceID: {deviceID}')
    TSP = 'ORT'
    retry_times = 0
    sfis=SFIS()
    sfis_data = sfis.Logout(sfis_op, deviceID, TSP)
    #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] logout: {sfis_data}')
    sfis_data = sfis.Login(sfis_op, deviceID, TSP)
    #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] login: {sfis_data}')
    while True:
        sfis_data = sfis.CheckRoute(SSN, deviceID)
        #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute: {sfis_data}')
        if sfis_data:
            if int(sfis_data[0]) == 1:
                #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>PASS<<')
                print('check route pass')
                return 0
            else:
                if "WRONG STEP" in sfis_data[1]:
                    sfis_error_msg = f'進錯站: {sfis_data[1]}'
                    #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>WRONG STEP<< : {sfis_data[1]}')
                    if retry_times < 1:
                        retry_times += 1
                        #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg
                elif 'ISN NOT INPUT' in sfis_data[1]:
                    sfis_error_msg = f'ISN未填: {sfis_data[1]}'
                    #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>ISN NOT INPUT<< : {sfis_data[1]}')
                    if retry_times < 1:
                        retry_times += 1
                        #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg

                else:
                    sfis_error_msg = f'check route fail: {sfis_data[1]}'
                    #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>FAIL<< : {sfis_data[1]}')
                    if retry_times < 1:
                        retry_times += 1
                        #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg    
        else:
            sfis_error_msg = f'check route fail, sfis_data error: {sfis_data[1]}'
            #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute >>FAIL DATA ERROR<< :{sfis_data[1]}')
            if retry_times < 1:
                retry_times += 1
                #SFIS_logger.debug(f'[SFIS check route] in [{deviceID}] chekroute retry: {retry_times}')
                continue
            else:
                return sfis_error_msg

def sfis_upload_thread():
    global dut_SSN_dic 
    global all_sfis_log 
    global all_sfis_error_code
    global sfis_deviceID

    ui_msg = dict()
    future_list = list() 
    umsg = ''
    #SFIS_logger.debug(f'[SFIS upload] get all_sfis_error_code: {all_sfis_error_code}, sfis_deviceID: {sfis_deviceID}, all_sfis_log: {all_sfis_log}')
    with ThreadPoolExecutor(max_workers=len(dut_SSN_dic)) as executor:
        for port, dut_ssn in dut_SSN_dic.items():
            futures = executor.submit(sfis_upload_flow, dut_ssn, all_sfis_error_code[port], sfis_deviceID[port], all_sfis_log[port])
            future_list.append(futures)
    
    for future in future_list:
        print(future.result())

    if umsg != '':
    
        return False
    return True


def sfis_upload_flow(SSN, error, deviceID, sfis_data, status = 1):
    #SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] get SSN: {SSN} , error: {error}, deviceID: {deviceID}, sfis_data: {sfis_data}')
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
                print(sfis_data)
                print(f"{SSN}PASS: {sfis_data[1]}")
                #SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload >>PASS<<')
                return 0
            else:
                if "WRONG STEP" in sfis_data[1]:
                    sfis_error_msg = f'進錯站: {sfis_data[1]}'
                    print(f"{SSN}進錯站: {sfis_data[1]}")
                    #SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload >>WRONG STEP<< :{sfis_data[1]}')
                    if retry_times < 1:
                        retry_times += 1
                        #SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg  
                else:
                    sfis_error_msg = f'SFIS upload failed: {sfis_data[1]}'
                    print(f"{SSN}error: {sfis_data[1]}")
                    #SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload >>FAIL<< :{sfis_data[1]}')
                    if retry_times < 1:
                        retry_times += 1
                        #SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload retry: {retry_times}')
                        continue
                    else:
                        return sfis_error_msg  
        else:
            sfis_error_msg = f'SFIS upload failed, sfis_data error: {sfis_data[1]}'
            print(f"{SSN}error: {sfis_data[1]}")
            #SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload >>FAIL SFIS DATA ERROR<< :{sfis_data[1]}')
            if retry_times < 1:
                retry_times += 1
                #SFIS_logger.debug(f'[SFIS upload] in [{deviceID}] upload retry: {retry_times}')
                continue
            else:
                return sfis_error_msg


if "__main__" == __name__:
    print(sfis_upload_thread())




