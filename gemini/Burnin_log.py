import os 
import time
import traceback
import sys
import datetime
from copy import deepcopy
import file_util


logfile_path = r'.\log'
logger_path = r'.\debug'
write_logger = file_util.create_logger(logger_path, 'write_log_log')

title_data = {'program_version' : 'V1.00.10', 
              'test_result' : 'Pass',
              'error_code' : '',
              'csn' : '',
              'terminal_connect_flag' : 'Pass',
              'dut_connect_flag' : '',
              'pg_connect_flag' : '',
              'start_time' : '',
              'end_time' : ''}

if not os.path.exists(logfile_path):
    os.mkdir(logfile_path)


def debug(func):
    def warpper(*args, **wargs):
        try:
            output_path = func(*args, **wargs)
        except Exception as ex:
            error_class = ex.__class__.__name__ #取得錯誤類型
            detail = ex.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2]#取得發生的函數名稱
            errMsg = f"{[error_class]}\n\"{fileName}\", line {lineNum}, in {funcName}\n{detail}"    
    return warpper


def write_terminal_server_log(**args):
    """
    Terminal server有問題時寫log
    """
    write_logger.debug('In [write_terminal_server_log]')
    global title_data
    reset_title_data()
    main_log = ''
    full_log = ''
    terminal_server_log = args['terminal_server_log']
    title_data['program_version'] = args['VERSION']

    terminal_server_log_test_list = list(terminal_server_log.keys())
    if 'fail_code' in terminal_server_log_test_list:
        title_data['error_code'] = terminal_server_log.pop('fail_code')
        terminal_server_log_test_list = list(terminal_server_log.keys())

    title_data['start_time'] = terminal_server_log[terminal_server_log_test_list[0]]
    title_data['end_time'] = terminal_server_log[terminal_server_log_test_list[-1]] 
    
    for test_name, test_data in terminal_server_log.items():
        if 'start' in test_name:
            main_log += start_and_end(test_name, test_data)
            main_log += '\n\n'
        
        if 'log' in test_name:
            main_log += test_data
            if test_data != '':
                main_log += '\n\n'
        
        if 'error' in test_name:
            title_data['test_result'] = 'Fail'
            main_log += error(test_data)
            main_log += '\n\n'
        
        if 'end' in test_name:
            main_log += start_and_end(test_name, test_data)
            main_log += '\n\n'

    full_log = write_title(full_log)
    full_log += main_log

    file_name = f"Terminal_server_{title_data['test_result']}_log"

    check_file_exist_and_write(file_name, full_log)
    reset_title_data()


def write_initial_log(**args):
    write_logger.debug('In [write_initial_log]')
    global title_data
    upload_file_path_list = list()
    reset_title_data()

    title_data['program_version'] = args['VERSION']
    total_dut_initial_log = args['total_dut_initial_log']
    write_logger.debug(f'total_dut_initial_log:{total_dut_initial_log}')
    dut_port_list = list(total_dut_initial_log.keys())

    all_sfis_log = args.get('all_sfis_log')
    
    
    all_sfis_error_code = args.get('all_sfis_error_code')


    for dut_port in dut_port_list:
        main_log =''
        full_log = ''
        package_sfis_log = ''
        dut_data = total_dut_initial_log[dut_port]
        dut_data_test_list = list(dut_data.keys())
        if 'fail_code' in dut_data_test_list:
            all_sfis_error_code[dut_port] = dut_data.get('fail_code')
            title_data['error_code'] = dut_data.pop('fail_code')
            dut_data_test_list = list(dut_data.keys())
        else:
            all_sfis_error_code[dut_port] = ''
        
        for test_name, test_data in list(dut_data.items()):
            if 'sfis_log' in test_name:
                dut_data.pop('sfis_log')
                all_sfis_log[dut_port] += test_data

        dut_data_test_list = list(dut_data.keys())        
        title_data['start_time'] = dut_data[dut_data_test_list[0]]
        title_data['end_time'] = dut_data[dut_data_test_list[-1]] 
        

        for test_name, test_data in dut_data.items():

            if 'start' in test_name:
                main_log += start_and_end(test_name, test_data)
                main_log += '\n\n'
        
            if 'log' in test_name:
                main_log += test_data
                if test_data != '':
                    title_data['dut_connect_flag'] = 'Pass'
                    main_log += '\n\n'
            
            if 'error' in test_name:
                title_data['test_result'] = 'Fail'
                if 'checkdutconnect_error' in test_name:
                    title_data['dut_connect_flag'] = 'Fail'
                main_log += error(test_data)
                main_log += '\n\n'
            
            if 'end' in test_name:
                main_log += start_and_end(test_name, test_data)
                main_log += '\n\n'   

        if args.get('pg_test_log'):
            pg_test_log = args['pg_test_log']
            pg_test_log_test_list = list(pg_test_log.keys())
            if 'fail_code' in pg_test_log_test_list:
                all_sfis_error_code[dut_port] = pg_test_log.get('fail_code')
                title_data['error_code'] = pg_test_log.pop('fail_code')
                pg_test_log_test_list = list(pg_test_log.keys())
            else:
                all_sfis_error_code[dut_port] = ''

            for test_name, test_data in list(pg_test_log.items()):
                if 'sfis_log' in test_name:
                    pg_test_log.pop('sfis_log')
                    package_sfis_log += test_data

            pg_test_log_test_list = list(pg_test_log.keys())

            title_data['end_time'] = pg_test_log[pg_test_log_test_list[-1]]
            for test_name, test_data in pg_test_log.items():
                if 'start' in test_name:
                    main_log += start_and_end(test_name, test_data)
                    main_log += '\n\n'
            
                if 'log' in test_name:
                    main_log += test_data
                    if test_data != '':
                        title_data['pg_connect_flag'] = 'True'
                        main_log += '\n\n'
                    else:
                        title_data['pg_connect_flag'] = 'Fail'
                
                if 'error' in test_name:
                    title_data['test_result'] = 'Fail'
                    main_log += error(test_data)
                    main_log += '\n\n'
                
                if 'end' in test_name:
                    main_log += start_and_end(test_name, test_data)
                    main_log += '\n\n' 
                                       

        if args.get('Nustream_test_log'):
            Nustream_test_log = args['Nustream_test_log']
            Nustream_test_log_list = list(Nustream_test_log.keys())
            if 'fail_code' in  Nustream_test_log_list:
                all_sfis_error_code[dut_port] = Nustream_test_log.get('fail_code')
                title_data['error_code'] = Nustream_test_log.pop('fail_code')
                Nustream_test_log_list = list(Nustream_test_log.keys())
            else:
                all_sfis_error_code[dut_port] = ''

            for test_name, test_data in list(Nustream_test_log.items()):
                if 'sfis_log' in test_name:
                    Nustream_test_log.pop('sfis_log')
                    package_sfis_log += test_data

            Nustream_test_log_list = list(Nustream_test_log.keys())


            title_data['end_time'] = Nustream_test_log[Nustream_test_log_list[-1]]
            for test_name, test_data in Nustream_test_log.items():
                if 'start' in test_name:
                    main_log += start_and_end(test_name, test_data)
                    main_log += '\n\n'
            
                if 'log' in test_name:
                    main_log += test_data
                    if test_data != '':
                        main_log += '\n\n'
                
                if 'error' in test_name:
                    title_data['test_result'] = 'Fail'
                    main_log += error(test_data)
                    main_log += '\n\n'
                
                if 'end' in test_name:
                    main_log += start_and_end(test_name, test_data)
                    main_log += '\n\n'

        all_sfis_log[dut_port] += package_sfis_log

        full_log = write_title(full_log)
        full_log += main_log
        full_log += sfis(all_sfis_log[dut_port])

        if 'serial_number' in dut_data_test_list:
            title_data['csn'] = dut_data['serial_number']
            model_name = dut_data['model_number']
            file_name = f"{deepcopy(title_data['csn'])}_ORT_Cycle_0_{deepcopy(title_data['program_version'])}_{deepcopy(title_data['test_result'])}"
            path = check_file_exist_and_write(file_name, full_log, model_name)
            upload_file_path_list.append((dut_port, path[0], path[1]))
        else:
            title_data['csn'] = f"DUT_{str(dut_port - 2002 +1)}"
            file_name = f"{deepcopy(title_data['csn'])}_ORT_Cycle_0_{deepcopy(title_data['program_version'])}_{deepcopy(title_data['test_result'])}"
            path = check_file_exist_and_write(file_name, full_log)
            upload_file_path_list.append((dut_port, path[0], path[1]))
        
        reset_title_data()
    
    upload_file_path_list = tuple(upload_file_path_list)
    return upload_file_path_list, all_sfis_log, all_sfis_error_code


def write_package_test_log(**args):
    write_logger.debug('In [write_package_test_log]')
    global title_data
    upload_file_path_list = []
    reset_title_data()
    package_log =''
    full_log = ''
    pack_sfis_log = ''

    title_data['program_version'] = args['VERSION']
    all_sfis_log = args.get('all_sfis_log')
    all_sfis_error_code = args.get('all_sfis_error_code')


    dut_data = args['dut_data']
    packaging_log = args['packaging_log']
    log_cycle = args['log_cycle']
    
    #write_logger.debug(f"packaging_log, {packaging_log}")
    package_times_list = list(packaging_log.keys())
    #write_logger.debug(f"package_times_list, {package_times_list}")
    dut_port_list = list(dut_data.keys())

    #先寫package的log，再加到其他dut的log裡面
    
    for times in package_times_list:
        package_log = package_log + 'Cycle : ' + str(times+1) + '\n'
        test_list = list(packaging_log[times].keys())
        #write_logger.debug(f"test_list, {test_list}")

        if 'fail_code' in test_list:
            sfis_error_code = packaging_log[times].get('fail_code')
            title_data['error_code'] = packaging_log[times].pop('fail_code')
            test_list = list(packaging_log[times].keys())
        else:
            sfis_error_code = ''

        for test_name, test_data in list(packaging_log[times].items()):
            if 'sfis_log' in test_name:
                packaging_log[times].pop('sfis_log')
                pack_sfis_log += test_data


        for test_name, test_data in packaging_log[times].items():
            if 'start' in test_name:  
                package_log += start_and_end(test_name, test_data)
                package_log += '\n\n'
    
            if 'log' in test_name:
                package_log += test_data
                if test_data != '':
                    package_log += '\n\n'
            
            if 'error' in test_name:
                title_data['test_result'] = 'Fail'
                package_log += error(test_data)
                package_log += '\n\n'
            
            if 'end' in test_name:
                package_log += start_and_end(test_name, test_data)
                package_log += '\n\n'

    package_times_list = list(packaging_log.keys())   
    test_list = list(packaging_log[times].keys())     
    title_data['start_time'] = packaging_log[package_times_list[0]][test_list[0]]
    title_data['end_time'] = packaging_log[package_times_list[-1]][test_list[-1]]
            
    for dut_port in dut_port_list:
        full_log= ''
        title_data['csn'] = dut_data[dut_port]['serial_number']
        model_name = dut_data[dut_port]['model_number']

        all_sfis_log[dut_port] += pack_sfis_log
        all_sfis_error_code[dut_port] = sfis_error_code

        full_log = write_title(full_log)
        full_log += package_log                
        full_log += sfis(pack_sfis_log)
        
        file_name = f"{deepcopy(title_data['csn'])}_ORT_Cycle_{str(log_cycle+1)}_{deepcopy(title_data['program_version'])}_{deepcopy(title_data['test_result'])}"
        path = check_file_exist_and_write(file_name, full_log, model_name)
        upload_file_path_list.append((dut_port, path[0], path[1]))
        
    upload_file_path_list = tuple(upload_file_path_list)
    return upload_file_path_list, all_sfis_log, all_sfis_error_code


def write_title(log):
    title = (f"Program Version : {title_data['program_version']}" +'\n'+ 
            f"Test Result : {title_data['test_result']}" + '\n' + 
            f"Error Code : {title_data['error_code']}" + '\n' + 
            f"CSN : {title_data['csn']}" + '\n' + 
            f"Terminal Connect flag: {title_data['terminal_connect_flag']}" + '\n'
            f"DUT Connection Flag: {title_data['dut_connect_flag']}" + '\n' + 
            f"PG Connect Flag: {title_data['pg_connect_flag']}" + '\n' +
            f"Start Time: {title_data['start_time']}" + '\n' + 
            f"End Time: {title_data['end_time']}" + '\n' + 
            '-' * 30 + '\n\n')
    
    log += title
    return log

def reset_title_data():
    global title_data
    title_data.clear()
    title_data = {'program_version' : 'V1.00.10', 
              'test_result' : 'Pass',
              'error_code' : '',
              'csn' : '',
              'terminal_connect_flag' : 'Pass',
              'dut_connect_flag' : '',
              'pg_connect_flag' : '',
              'start_time' : '',
              'end_time' : ''}


def start_and_end(state, time):
    state = state.split('_')[0].upper() + ' '+ state.split('_')[1].upper()
    time = time.split(' ')[1]
    string = ('-'*25 + '\n' + 
            f'[{state}] {time}' + '\n' + '-'*25)
    return string

def sfis(sfis_log):
    string = ('\n'*5 + '-'*25 + 'SFIS' + '-'*25 + '\n' + sfis_log)
    return string


def error(value):
    string = ('*' * 30 + '\n' + 
            f'ERROR MESSAGE : {value}' + '\n' +
            '*' * 30 + '\n')
    return string
    

def check_file_exist_and_write(filename, log, model_name = None):
    now = datetime.datetime.now()
    nowdatetime = now.strftime('%Y-%m-%d')

    filename_txt = f"{filename}.txt"

    if model_name:
        log_folder_path = rf"{logfile_path}\{model_name}\{nowdatetime}"
    else:
        log_folder_path = rf"{logfile_path}\uncategorized\{nowdatetime}"
    os.makedirs(log_folder_path, exist_ok=True)

    file_repeat_num = 0
    while True:
        log_path = os.path.join(log_folder_path, filename_txt)
        if os.path.isfile(log_path):
            file_repeat_num += 1
            filename_txt = f"{filename}_{file_repeat_num}.txt"
        else:
            break
    
    with open(log_path, 'w+', newline='', encoding="utf-8") as f:
        f.write(log)
    write_logger.debug(f'write log done: {log_path}')

    ftp_path = "/".join(log_path.split('\\')[len(logfile_path.split('\\')):-1])

    return (log_path, ftp_path)












if "__main__" == __name__:
    pass









