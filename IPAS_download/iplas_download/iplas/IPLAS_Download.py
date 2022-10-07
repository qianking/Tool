from copy import deepcopy
from glob import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from IPLAS_Download_flow import IPLAS_Flow
import threading
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
import shutil
import re
import time
import os
import sys
import traceback
import datetime
import lib.create_log as create_log
import lib.Excel_barchart as excel_report


main_data = {'userdata': ['Andy_Chien', 'pega#654321654321'], 
             'chrome_driver_path': r'd:\Qian\python\GIT\Tool\IPAS_download\iplas_download\docs\chromedriver.exe', 
             'root_path': 'D:\\IPLAS Download'}   #外部傳進來  外面先創好資料夾，如果沒有D槽，那就創在C槽

execute_data = {'site':'蘇州',
                'data_source':'Test Station',
                'user_select_project': 'SWITCH_CISCO_EZ1KA1',   
                'time_selection':{'time':'Select Manually', 'time_period':['2022/08/28 00:00', '2022/08/28 10:00']}}  #UI傳入  #['Current Shift', 'Today', 'This Week', 'A Week', 'YTD Day Shift', 'YTD Night Shift', 'Select Manually']

current_path = os.path.dirname(os.path.abspath(__file__))       #目前檔案的絕對路徑
upper_folder_path = '\\'.join(current_path.split('\\')[:-1])     #到上一層資料夾

IPLAS_download_buffer = fr"{upper_folder_path}\IPLAS_Download\buffer"        #IPLAS下載檔案buffer的資料夾
os.makedirs(IPLAS_download_buffer, exist_ok=True)

IPLAS_download_log = fr"{upper_folder_path}\logs\IPLAS download"  #存IPLAS下載log的資料夾
os.makedirs(IPLAS_download_log, exist_ok=True)

IPLAS_download_log_file = fr"{IPLAS_download_log}\IPLAS_download_log.txt"
Download_logger = create_log.create_logger(IPLAS_download_log_file, f'IPLAS_download_log')
#Download_logger.disabled = True  #禁用log

threadLocal = threading.local()
rlock = threading.RLock()
driver_count = 1  #用在編號drivers
driver_data = dict()
all_data =dict()

ui_signal = None


def get_data_from_UI(data, signal):
    global execute_data
    global ui_signal
    execute_data = data
    ui_signal = signal

def send_to_UI(txt):
    ui_signal.status.emit(txt)


def get_now_daytime():
    now = datetime.datetime.now()
    nowdatetime = now.strftime('%Y-%m-%d %H-%M')
    return nowdatetime


def clear_folder(folder_path):
    file_list = glob(f"{folder_path}\*")
    if len(file_list):
        for file in file_list:
            try:
                os.remove(file)
            except:
                shutil.rmtree(file)

def create_today_download_file():
    nowdatetime = get_now_daytime()
    today_download_file = f"{nowdatetime} {execute_data['user_select_project']}"
    today_download_path = fr"{main_data['root_path']}\{today_download_file}"
    #today_download_path = fr"{upper_folder_path}\IPLAS_Download\{today_download_file}"
    os.makedirs(today_download_path, exist_ok=True)
    all_data['today_download_path'] = today_download_path


def set_chrome_driver():
    servic = Service(main_data['chrome_driver_path'])
    options = Options()
    #options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("detach", True)   
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  
    prefs = {"download.default_directory": IPLAS_download_buffer,
            "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option("prefs",prefs)
    #options.add_argument("--headless") #設定無視窗模式
    driver =  webdriver.Chrome(service = servic, options = options)
    return driver

#threadLocal原理為，將每個線程的變數以對應的線程ID和對應的變數保存到一個全局的字典裡，如果那個線程要拿變數的話，就去對應的線程ID拿取相對應的數據
#我們使用線程池，代表所有的線程就是三個線程在輪流執行，所以同一個線程中(同一個線程ID)可以拿取上次執行完的dirver((同一個線程ID，同一個driver)繼續執行
def get_IPLAS():
    driver =  getattr(threadLocal, 'driver', None)  #去threadLocal拿driver
    if driver is None: #如果拿不到driver
        driver = set_chrome_driver() #設置新driver
        rlock.acquire()
        global driver_data
        global driver_count
        driver_data[driver] = driver_count  #driver編號
        driver_count += 1
        rlock.release()
        setattr(threadLocal, 'driver', driver) #設置新driver
    IPLAS = IPLAS_Flow(driver, Download_logger, driver_data)
    return IPLAS

#檢查個測站中pass/fail是否有數值，如果都沒有的話傳回false
def check_station_data(data):
    have_data_flage = False
    for station, datas in data.items():
        for pf, num in datas.items():
            if num:
                have_data_flage = True
                break
    return have_data_flage


#用來合併字典面有字典的字典
def dict_of_dict_merge(x, y):
    z = {}
    overlapping_key = x.keys() & y.keys()
    for key in overlapping_key:
        z[key] = dict_of_dict_merge(x[key], y[key])
    for key in x.keys() - overlapping_key:
        z[key] = deepcopy(x[key])
    for key in y.keys() - overlapping_key:
        z[key] = deepcopy(y[key])
    return z

def merge_dic(data_dic):
    station_list = list(all_data['station_data'].keys())
    for station in station_list:
        all_data['station_data'][station]['ISN_data'] = data_dic[station] if data_dic.get(station) else None

def add_path_to_data(test_station, isn, isn_data, txt_file_path):
    root_len = len(all_data['today_download_path'].split('\\'))
    txt_file_path = '\\'.join(txt_file_path.split('\\')[root_len:])
    org_list = ['fail_list', 'retest_list', 'error_count_data']
    test_station = re.sub("[ ]", "_", test_station)
    for name in org_list:
        data = all_data['station_data'][test_station]['ISN_data'][isn_data[-1]][name]
        if isn in data:
            data[f"{isn} {isn_data[2]}"] = txt_file_path
    #else:
       #shutil.rmtree('\\'.join(path.split('\\')[:-1]))
        

#將所有ISN合併成一個大list
def get_all_isn_list(station_data):
    isn_list = []
    for station, data in station_data.items():
        isn_data = data['ISN_data']
        if isn_data:
            for test_item, data_dic in isn_data.items():
                isn_list.extend(list(data_dic['error_count_data'].keys()))
            
    isn_list = tuple(set(isn_list))
    return isn_list

def organize_station_data():
    org_list = ['fail_list', 'retest_list', 'error_count_data']
    station_data = all_data['station_data']
    all_data['excel_data'] = {}
    for station, data in station_data.items():
        max_fail_num = 0
        max_retest_pass_num = 0
        max_error_count = 0
        final_fail_num = 0
        final_pass_num = 0
        isn_data = data['ISN_data']
        if isn_data:
            for test_item, test_data in isn_data.items():
                final_fail_num += int(test_data['fail_num'])
                final_pass_num += int(test_data['retest_pass_num'])
                for name in org_list:
                    for isn in test_data[name].copy():
                        if not test_data[name][isn]:
                            del test_data[name][isn]

                max_fail_num = len(test_data['fail_list']) if len(test_data['fail_list']) > max_fail_num else max_fail_num
                max_retest_pass_num = len(test_data['retest_list']) if len(test_data['retest_list']) > max_retest_pass_num else max_retest_pass_num
                max_error_count = len(test_data['error_count_data']) if len(test_data['error_count_data']) > max_error_count else max_error_count

                error_count_path = list(test_data['error_count_data'].values())[0]
                error_count_path = '\\'.join(error_count_path.split('\\')[:-2])
                test_data['error_count_path'] = error_count_path
    
        all_data['excel_data'][station] = {'max_error_count':max_error_count, 'max_fail_num':max_fail_num, 'max_retest_pass_num':max_retest_pass_num}
        data['final_fail_num'] = final_fail_num
        data['final_pass_num'] = final_pass_num
        

#region 移動檔案和解壓縮
def move_isn_file(type, file_list, all_isn_data):
    for isn_file_data in all_isn_data[:]:
        isn = isn_file_data['isn']  
        isn_datas = isn_file_data['isn_data']  #得到isn_data ex:('991982', '(QSFCG4)', '08/09 18:19:25', 'IOS Boot Up') 
        for isn_data in isn_datas[:]:
            file_name_pattern = get_name_pattern(type, isn_data, isn)
            for file_path in file_list[:]:
                find_file = file_name_pattern.findall(file_path)
                if len(find_file):
                    if type == 'zip':
                        unzip_zip_file_and_move(file_path, find_file, isn_data, isn)
                    if type == 'csv':
                        move_csv_file(file_path, find_file, isn_data, isn)
                    isn_datas.remove(isn_data)
                    file_list.remove(file_path)
                    time.sleep(0.1)
                    if not len(isn_datas):
                        all_isn_data.remove(isn_file_data)
                    break
                    
    return all_isn_data

def get_name_pattern(type, isn_data, isn):
    if type == 'zip':
        file_time = re.sub("[/:]", "_", isn_data[2]) #將isn_data裡面的時間那欄(2)中出現的'/'和':'以'_'換掉
        file_name_pattern = re.compile(rf"{execute_data['user_select_project']}_(.*)_({isn_data[0]}_\d\d\d\d_{file_time})", re.I)
    if type == 'csv':
        file_time = re.sub("[/:]", "", isn_data[2])
        file_time = re.sub("[ ]", "_", file_time)
        file_name_pattern = re.compile(rf"{isn}_(.*)_{isn_data[0]}(-[0-9])*_(\w+)_(\w+){file_time}", re.I)
    return file_name_pattern

def unzip_zip_file_and_move(zip_file_path, find_file, isn_data, isn):
    upper_path = '\\'.join(zip_file_path.split('\\')[:-1]) #得到上一層路徑
    test_station = find_file[0][0]  #得到測站

    test_item = re.sub("[/: \\*?<>|-]", "_", isn_data[-1])  #將測試項目格式轉換
    deviceid_time = find_file[0][1] 

    move_to_file_path = f"{all_data['today_download_path']}\{test_station}\{test_item}"
    os.makedirs(move_to_file_path, exist_ok=True) 
    Download_logger.debug(f"create folder [{move_to_file_path}]") 

    unzip_folder_name = f"{isn}_{deviceid_time}"    #組合成 isn_deciceid_time 格式資料夾
    with ZipFile(zip_file_path, 'r') as zip:        #先解壓縮到原下載資料夾
        zip.extractall(f"{upper_path}\{unzip_folder_name}")
    Download_logger.debug(f"unzip zip file [f'{upper_path}\{unzip_folder_name}'] -> [{move_to_file_path}]")

    #csv檔案需先在下載資料夾改名子完再移動資料夾
    csv_file_path = glob(f"{upper_path}\{unzip_folder_name}\*.csv")[0]
    rename_csv(csv_file_path)   #csv檔案重新命名，以免黨名太長打不開
    shutil.move(f"{upper_path}\{unzip_folder_name}", move_to_file_path)
    Download_logger.debug(f"move folder [f'{upper_path}\{unzip_folder_name}'] -> [{move_to_file_path}]") 

    txt_file_path = glob(f"{move_to_file_path}\{unzip_folder_name}\*.txt")[0]
    add_path_to_data(test_station, isn, isn_data, txt_file_path)

    os.remove(zip_file_path)    

def move_csv_file(csv_file_path, find_file, isn_data, isn):
    test_station = find_file[0][0].split('_')[-1] #得到 isn 跟 deviceid 之間的文字，以"_"分開之後最後一個為測試站
    test_item = re.sub("[/: \\*?<>|-]", "_", isn_data[-1])   #把test item裡面的空白換成"_"
    test_time = f"{find_file[0][-1]}_{re.sub('[/:]', '_', isn_data[2])}"  #find_file[0][-1]: 年, isn_data[2]: 檔案時間

    file_folder_name = f"{isn}_{isn_data[0]}_{test_time}"  #組合成 isn_deciceid_time 格式資料夾
    move_to_file_path = f"{all_data['today_download_path']}\{test_station}\{test_item}\{file_folder_name}" 
    os.makedirs(move_to_file_path,  exist_ok=True)
    Download_logger.debug(f"create folder [{move_to_file_path}]") 

    #csv檔案需先在下載資料夾改名子完再移動資料夾
    new_path = rename_csv(csv_file_path)
    shutil.move(new_path, move_to_file_path)

    add_path_to_data(test_station, isn, isn_data, move_to_file_path)

    Download_logger.debug(f"move csv file [{csv_file_path}] -> [{move_to_file_path}]") 
    

def rename_csv(csv_file_path):
    csv_file_name = csv_file_path.split("\\")[-1]     #得到csv黨名
    new_csv_file_name = f"{csv_file_name.split('_')[0]}.csv" #csv檔案重新命名，以免檔名太長打不開
    new_path = csv_file_path.replace(csv_file_name, new_csv_file_name)
    os.rename(csv_file_path, new_path)
    return new_path
    
#endregion

def move_and_unzip_isn_file(isn_data):
    error_list = list()
    zip_file_list = glob(f"{IPLAS_download_buffer}\*.zip")
    csv_file_list = glob(f"{IPLAS_download_buffer}\*.csv")
    
    data = move_isn_file('zip', zip_file_list, isn_data)
    if len(data) and len(csv_file_list):
        data = move_isn_file('csv', csv_file_list, data)
    elif len(data):
        error_list = data

    file_list = glob(f"{IPLAS_download_buffer}\*")

    if len(file_list):
        print('偵測到多餘檔案: {file_list}')
        Download_logger.debug(f"detect undownload file: {file_list}") 

    if len(error_list):
        print('有檔案未下載到: {error_list}')
        ReDownload_ISN(error_list)
        move_and_unzip_isn_file(error_list)
        Download_logger.debug(f"have undownload isn file: {error_list}")  
         
    else:
        print("執行完成")
        Download_logger.debug(f"download complete")

#用來顯示花費時間
def timer_and_debug(func):
    def warp(*warp, **awage):
        start_time = time.time()
        try:
            func(*warp, **awage)
            
        except Exception as ex:
            error_class = ex.__class__.__name__ #取得錯誤類型
            detail = ex.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastcallstack = traceback.extract_tb(tb)[-1]#取得Call Stack的最後一筆資料
            fileName = lastcallstack[0] #取得發生的檔案名稱
            lineNum = lastcallstack[1] #取得發生的行號
            funcName = lastcallstack[2] #取得發生的函數名稱
            error_txt = f"[ERROR TYPE] {error_class}\n[ERROR DETAIL] {detail}\n[ERROR PATH] in file \"{fileName}\", line {lineNum}, function [{funcName}]"
            print(error_txt)
            ui_signal.error.emit(error_txt)
            Download_logger.exception('exception:')
            return 0  

        finally:
            for driver in driver_data:  #關掉driver
                driver.close()
            end_time = time.time()
            print(f'cost time {end_time-start_time}')
    return warp

@timer_and_debug
def Main_Download(data, signal):
    get_data_from_UI(data, signal)
    clear_folder(IPLAS_download_buffer)  #清除download buffer裡面的檔案
    create_today_download_file()  #建立以'月-日 小時-分鐘_下載project' 為名子的資料夾
    isn_data = Start_Thread_main()
    ''' with open(r'D:\Qian\python\GIT\Tool\IPAS_download\iplas_download\IPLAS_Download\isn_data.txt', 'w+') as f:
        f.write(json.dumps(isn_data)) '''
    if isn_data:
        move_and_unzip_isn_file(isn_data)
        organize_station_data()
    ''' with open(r'D:\Qian\python\GIT\Tool\IPAS_download\iplas_download\IPLAS_Download\data.txt', 'w+') as f:
        f.write(json.dumps(all_data)) '''
    print(all_data)
    excel_report.excel_wrtting_flow(all_data, execute_data) 
    #print('\nall_data', all_data)


def Start_Thread_main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        station_data = Get_Station_Data(executor)
        if check_station_data(station_data):
            error_tmp_data = Get_PassFail_ISN(executor, station_data)
            station_data = Get_Error_Data(executor, error_tmp_data)
            isn_data = Download_ISN_File(executor, station_data)
            #print('\nisn_data',isn_data)
            #isn_data = None
            return isn_data
        else:
            print('此時間段沒數據')
                
    for driver in driver_data:  #關掉driver
        driver.close()
    

def Get_Station_Data(executor):
    '''
    去拿取個測站名稱以及pass/fail個數
    '''
    global all_data
    futures = [executor.submit(Login_Flow, ) for i in range(3)]   #三個瀏覽器登入
    futures = executor.submit(Get_Station_Data_Flow, )  #其中一個去拿測站的資訊
    exception = futures.exception()
    if not exception:
        data = futures.result()  #傳回測站的名子和pass fail個數
        all_data['station_data'] = data.pop('station_data')
        all_data['iplas_data'] = data
        station_data = deepcopy(all_data['station_data'])
        return station_data
    else:
        send_to_UI(f'Exception! Please see the download log: \n{IPLAS_download_log_file}')
        raise Exception(exception)
    

def Get_PassFail_ISN(executor, station_data):
    '''
    拿取各測站fail中所有的測項中fail/retest個數以及ISN名單
    '''
    tmp_dic = {}
    error_tmp_data = {}
    station_list = [key for key in station_data.keys() if station_data[key]['fail_num']]     #傳入有fail數目的測站
    datas = [executor.submit(Get_PassFail_ISN_Flow, station) for station in station_list]    #得到各測站fail的isn名單
    for data in datas: 
        exception = data.exception()
        if not exception:
            error_tmp_data.update(data.result().pop('error_tmp_data'))
            tmp_dic.update(data.result())
        else:
            send_to_UI(f'Exception! Please see the download log: \n{IPLAS_download_log_file}')
            raise Exception(exception)
    merge_dic(tmp_dic)
    return error_tmp_data


def Get_Error_Data(executor, error_tmp_data):
    '''
    拿取error count裡面遺漏的isn data
    '''
    global all_data
    error_url_list = list(error_tmp_data.keys())
    datas = [executor.submit(Get_Error_Data_Flow, error_url) for error_url in error_url_list]
    for data in datas:
        exception = data.exception()
        if not exception:
            url = data.result()['error_url']
            url_data = error_tmp_data[url]
            error_data = data.result()['error_data']
            all_data['station_data'][url_data.split('+')[0]]['ISN_data'][url_data.split('+')[1]]['error_count_data'] = error_data
        else:
            send_to_UI(f'Exception! Please see the download log: \n{IPLAS_download_log_file}')
            raise Exception(exception)

    return all_data['station_data']


def Download_ISN_File(executor, station_data):
    '''
    傳入isn來獲取各isn裡面的所有資料以及下載檔案
    '''
    isn_data = []
    isn_list = get_all_isn_list(station_data)   #得到retest跟fail的isn名單
    datas = [executor.submit(Download_ISN_File_Flow, isn) for isn in isn_list]   #下載retest isn列表裡的檔案
    for data in datas:
        exception = data.exception()
        if not exception:
            isn_data.append(data.result())      #('995548', '(QSFC09)', '08/15 21:47:08', 'Loopback Test-SFP 1G Link TEST')
        else:
            send_to_UI(f'Exception! Please see the download log: \n{IPLAS_download_log_file}')
            raise Exception(exception)

    return isn_data



def ReDownload_ISN(isn_datas):
    driver = set_chrome_driver()
    IPLAS = IPLAS_Flow(driver, Download_logger)
    IPLAS.Login_IPLAS(main_data['userdata'])
    for isn_data in isn_datas:
        IPLAS.ReDownload_ISN_File(execute_data['user_select_project'], isn_data)
        if IPLAS.exception:
            raise Exception(IPLAS.exception) 

def Login_Flow():
    IPLAS = get_IPLAS()
    IPLAS.Login_IPLAS(main_data['userdata'])
    if IPLAS.exception:
        raise Exception(IPLAS.exception)

def Get_Station_Data_Flow():
    IPLAS = get_IPLAS()
    IPLAS.Get_User_Project()
    IPLAS.Jump_to_Project_page(execute_data['user_select_project'])
    IPLAS.Get_Time_Option()
    IPLAS.Choose_Line_View()
    IPLAS.Choose_Time(execute_data['time_selection'])
    IPLAS.Get_Necessary_Parameter()
    IPLAS.Get_Stationname_and_PassFail()
    if IPLAS.exception:
        raise Exception(IPLAS.exception)
    else:
        return IPLAS.iplas_data

def Get_PassFail_ISN_Flow(station):
    IPLAS = get_IPLAS()
    IPLAS.Get_PassFail_ISN(station, execute_data['user_select_project'], all_data['iplas_data']['queryid'])
    if IPLAS.exception:
        raise Exception(IPLAS.exception)
    else:
        return IPLAS.iplas_data


def Get_Error_Data_Flow(error_url):
    IPLAS = get_IPLAS()
    IPLAS.Get_Error_Data(error_url)
    if IPLAS.exception:
        raise Exception(IPLAS.exception)
    else:
        return IPLAS.iplas_data


def Download_ISN_File_Flow(isn):
    IPLAS = get_IPLAS()
    IPLAS.Download_ISN_File(execute_data['user_select_project'], isn)
    if IPLAS.exception:
        raise Exception(IPLAS.exception)
    else:
        return IPLAS.iplas_data

def _test():
    driver = set_chrome_driver()
    driver_data[driver] = 1
    IPLAS = IPLAS_Flow(driver, Download_logger, driver_data)
    IPLAS.Login_IPLAS(main_data['userdata'])
    IPLAS.Get_User_Project()
    IPLAS.Jump_to_Project_page(execute_data['user_select_project'])
    IPLAS.Get_Time_Option()
    IPLAS.Choose_Line_View()
    IPLAS.Choose_Time(execute_data['time_selection'])
    IPLAS.Get_Necessary_Parameter()
    IPLAS.Get_Stationname_and_PassFail()
    if IPLAS.exception:
        raise Exception(IPLAS.exception)
    
    #IPLAS.Download_ISN_File(execute_data['user_select_project'], isn = '2259943802782')
    ''' IPLAS.Get_User_Project()
    IPLAS.Jump_to_Project_page(execute_data['user_select_project'])
    IPLAS.Get_Time_Option()
    IPLAS.Choose_Time(execute_data['time_selection']) '''
    """IPLAS.Get_Necessary_Parameter()
    IPLAS.Get_Stationname_and_PassFail()
    iii = IPLAS.iplas_data
    print(IPLAS.iplas_data)
    staton_data = IPLAS.Get_PassFail_ISN('Pretest', execute_data['user_select_project'], iii['queryid'])
    print(staton_data)"""
   
def Get_User_Project(signal):
    driver = set_chrome_driver()
    IPLAS = IPLAS_Flow(driver, Download_logger)
    IPLAS.Login_IPLAS(main_data['userdata'])
    IPLAS.Get_User_Project()
    if IPLAS.exception:
        raise Exception(IPLAS.exception)
    else:
        driver.close()
        signal.status.emit("finish")
        return IPLAS.iplas_data


if __name__ == "__main__":
    isn_datas = [{"isn": "2259346202964", "isn_data": [["991952", "(QSFCG4)", "08/28 05:06:58", "DUT Reload TIME OUT"]]}, 
                {"isn": "2259346200570", "isn_data": [["620886", "(QSFC38)", "08/28 05:36:51", "Combo copper-prefer setup"]]},]
    #Main_Download(execute_data)
    #ReDownload_ISN(isn_datas)
    #move_and_unzip_isn_file(isn_data)
    #organize_station_data()
    #print('\nall_data', all_data)
    _test()