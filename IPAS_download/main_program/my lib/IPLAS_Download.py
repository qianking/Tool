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
import datetime
import create_log


main_data = {'userdata': ['Andy_Chien', 'Qianking0706-'], 
             'chrome_driver_path': r'D:\Qian\python\GIT\Tool\IPAS_download\main_program\data\chromedriver.exe'}   #外部傳進來

execute_data = {'user_select_project': 'SWITCH_CISCO_EZ1KA1',   
                'time_selection':{'time':'Today', 'time_period':['2022/07/25 08:00', '2022/08/05 08:00']}}  #UI傳入  #['Current Shift', 'Today', 'This Week', 'A Week', 'YTD Day Shift', 'YTD Night Shift', 'Select Manually']

current_path = os.path.dirname(os.path.abspath(__file__))       #目前檔案的絕對路徑
upper_folder_path = '\\'.join(current_path.split('\\')[:-1])     #到上一層資料夾

IPLAS_download_buffer = fr"{upper_folder_path}\IPLAS_Download\buffer"        #IPLAS下載檔案buffer的資料夾
os.makedirs(IPLAS_download_buffer, exist_ok=True)

IPLAS_download_log = fr"{upper_folder_path}\logs\IPLAS download"  #存IPLAS下載log的資料夾
os.makedirs(IPLAS_download_buffer, exist_ok=True)

IPLAS_download_log_file = fr"{IPLAS_download_log}\IPLAS_download_log.txt"
Download_logger = create_log.create_logger(IPLAS_download_log_file, f'IPLAS_download_log')
Download_logger.disabled = True

threadLocal = threading.local()
rlock = threading.RLock()
driver_count = 1  #用在編號drivers
driver_data = {}
iplas_data = {}
data = {'fail_isn': [], 'retest_isn_list': [{'isn': '2263431002642', 'isn_data': [('995548', '(QSFI37)', '08/11 01:34:34', 'Battery 3V3 Test')]}, 
        {'isn': '2260813003990', 'isn_data': [('620893', '(QSFT0P)', '08/09 19:42:20', 'PG Test')]}, 
        {'isn': '2260813003301', 'isn_data': [('995589', '(QSFI26)', '08/08 09:37:43', 'Power Test P44')]}, 
        {'isn': '2260813003295', 'isn_data': [('991982', '(QSFT15)', '08/08 15:08:51', 'eeprom save')]}, 
        {'isn': '2260813001576', 'isn_data': [('991072', '(QSFT33)', '08/08 09:57:59', 'Copy Flash File to BS')]}, 
        {'isn': '2260813003963', 'isn_data': [('991034', '(QSFCG4)', '08/09 17:37:53', 'IOS Boot Up')]}, 
        {'isn': '2260813003363', 'isn_data': [('995589', '(Q0FT18)', '08/08 09:51:18', 'DUT Timeout')]}, 
        {'isn': '2260813002946', 'isn_data': [('991072', '(QSFCG4)', '08/09 16:42:05', 'IOS Boot Up')]}, 
        {'isn': '2259346000661', 'isn_data': [('991072', '(QSFCG4)', '08/10 21:29:34', 'DUT Reload TIME OUT')]}, 
        {'isn': '2260813002778', 'isn_data': [('620893', '(QSFI02)', '08/09 04:36:26', 'MOUNT USB Check')]}, 
        {'isn': '2260813000642', 'isn_data': [('991043', '(QSFT33)', '08/08 11:23:18', 'Copy Flash File to BS')]}, 
        {'isn': '2259346000212', 'isn_data': [('995547', '(QSFI37)', '08/09 18:27:06', 'Battery 3V3 Test')]}, 
        {'isn': '2260813003181', 'isn_data': [('995596', '(Q0FT18)', '08/08 18:32:39', 'SFIS Get Timer')]}, 
        {'isn': '2259346000491', 'isn_data': [('991952', '(QSFT15)', '08/10 21:48:37', 'IOS Ping Check')]}, 
        {'isn': '2260813003519', 'isn_data': [('991048', '(QSFCG4)', '08/09 14:58:48', 'IOS Boot Up')]}, 
        {'isn': '2260813003595', 'isn_data': [('620886', '(Q0FT18)', '08/09 14:13:34', 'DUT Timeout')]}, 
        {'isn': '2260813003043', 'isn_data': [('991036', '(QSFCG4)', '08/09 04:39:33', 'DUT Bootloader Reset TIME OUT')]}, 
        {'isn': '2260813003279', 'isn_data': [('991042', '(QSFCG4)', '08/08 18:30:35', 'DUT Bootloader Reset TIME OUT')]}, 
        {'isn': '2260813000609', 'isn_data': [('991042', '(QSFT33)', '08/08 12:45:04', 'Copy Flash File to BS')]}, 
        {'isn': '2260813003738', 'isn_data': [('620886', '(QSFC38)', '08/08 17:44:46', 'combo show')]}, 
        {'isn': '2260813002739', 'isn_data': [('620886', '(QSFC38)', '08/08 17:02:32', 'combo show')]}, 
        {'isn': '2260813001009', 'isn_data': [('620886', '(QSFT27)', '08/09 17:00:19', 'ControlBoard Hook Power ON')]}, 
        {'isn': '2260813003176', 'isn_data': [('991944', '(QSFCG4)', '08/09 15:31:33', 'IOS Boot Up')]}, 
        {'isn': '2259943800081', 'isn_data': [('995593', '(QSFC09)', '08/10 07:02:46', 'Loopback Test-RJ 1G Link TEST')]}, 
        {'isn': '2260813000718', 'isn_data': [('991982', '(QSFCG4)', '08/09 09:02:58', 'DUT Reload TIME OUT')]}, 
        {'isn': '2260813002352', 'isn_data': [('991036', '(QSFT15)', '08/09 03:54:57', 'IOS Ping Check')]}, 
        {'isn': '2260813002837', 'isn_data': [('991043', '(QSFCG4)', '08/09 11:31:17', 'DUT Reload TIME OUT')]}, 
        {'isn': '2260813000342', 'isn_data': [('991072', '(QSFCG4)', '08/09 04:39:35', 'DUT Bootloader Reset TIME OUT')]}, 
        {'isn': '2260813002612', 'isn_data': [('991036', '(QSFT33)', '08/09 16:24:10', 'Copy Flash File to BS')]}, 
        {'isn': '2260813000601', 'isn_data': [('991042', '(QSFCG4)', '08/08 10:48:31', 'IOS Boot Up')]}, 
        {'isn': '2260813000608', 'isn_data': [('991034', '(QSFCG4)', '08/08 10:28:17', 'DUT Bootloader Reset TIME OUT')]}, 
        {'isn': '2260813000073', 'isn_data': [('991042', '(QSFT15)', '08/09 14:57:25', 'Archive IOS')]}, 
        {'isn': '2260813001258', 'isn_data': [('991042', '(QSFT15)', '08/09 09:24:14', 'IOS Initial Dialog')]}, 
        {'isn': '2260813003323', 'isn_data': [('991991', '(QSFCG4)', '08/09 18:22:19', 'IOS Boot Up')]}, 
        {'isn': '2259346000233', 'isn_data': [('995547', '(QSFF11)', '08/09 17:07:33', 'Pegatron MFG Version'), ('620841', '(QSFF11)', '08/10 01:22:27', 'Pegatron MFG Version')]}, 
        {'isn': '2260813001901', 'isn_data': [('620893', '(QSFT27)', '08/09 01:20:05', 'ControlBoard Hook Power ON')]}, 
        {'isn': '2260813003140', 'isn_data': [('991072', '(QSFCG4)', '08/09 14:29:38', 'DUT Bootloader Reset TIME OUT')]}, 
        {'isn': '2202143400152', 'isn_data': [('991944', '(QSFT15)', '08/10 09:25:28', 'Press Enter')]}, 
        {'isn': '2260813003429', 'isn_data': [('620886', '(QSFT27)', '08/09 01:20:05', 'ControlBoard Hook Power ON')]}, 
        {'isn': '2259943801588', 'isn_data': [('620886', '(Q0FT18)', '08/10 23:33:16', 'SFP_1 module detect Info')]}, 
        {'isn': '2259346000924', 'isn_data': [('995547', '(QSFL06)', '08/09 18:38:33', 'Check Green LED Color')]}, 
        {'isn': '226492180000004', 'isn_data': [('995548-1', '(QSFB03)', '08/11 01:53:41', 'Check BATT')]}, 
        {'isn': '2259346000508', 'isn_data': [('991952', '(QSFT15)', '08/10 21:29:50', 'IOS Ping Check')]}, 
        {'isn': '2259943801441', 'isn_data': [('620886', '(Q0FT18)', '08/11 01:53:02', 'SFP_2 module detect Info'), ('620834', '(QSFT15)', '08/11 03:07:25', 'DUT Turn On')]}, 
        {'isn': '2260813000459', 'isn_data': [('620832', '(QSFT53)', '08/08 10:38:01', 'Enter Console')]}, 
        {'isn': '2260813003389', 'isn_data': [('620832', '(QSFT15)', '08/08 23:33:26', 'System Info Check')]}, 
        {'isn': '2260813003592', 'isn_data': [('995588', '(QSFC09)', '08/09 01:38:34', 'Loopback Test-RJ 1G Link TEST')]}, 
        {'isn': '2259346000427', 'isn_data': [('620893', '(QSFC35)', '08/10 02:19:52', 'Port 0/4 LinkUP')]}, 
        {'isn': '2260813003305', 'isn_data': [('620832', '(QSFT15)', '08/09 05:31:50', 'DUT Turn On')]}, 
        {'isn': '2260813002448', 'isn_data': [('620834', '(QSFC03)', '08/08 15:52:29', 'Ping Cisco Server Retry 1')]}, 
        {'isn': '2260813003566', 'isn_data': [('995589', '(QSFC09)', '08/08 09:56:52', 'Loopback Test-SFP 1G Link TEST')]}, 
        {'isn': '2260813002943', 'isn_data': [('991944', '(QSFCG4)', '08/09 11:35:03', 'DUT Reload TIME OUT')]}, 
        {'isn': '2260813003489', 'isn_data': [('995596', '(Q0FT18)', '08/09 03:06:46', 'SFIS Get Timer')]}, 
        {'isn': '2260813003408', 'isn_data': [('991048', '(QSFT33)', '08/09 23:07:09', 'Copy Flash File to BS TIME OUT')]}, 
        {'isn': '2259346000740', 'isn_data': [('995547', '(QSFL06)', '08/09 18:22:07', 'Check Green LED Color')]}, 
        {'isn': '2260813003111', 'isn_data': [('620835', '(QSFT15)', '08/09 18:35:07', 'DUT Turn On')]}, 
        {'isn': '2260813002922', 'isn_data': [('991053', '(QSFT15)', '08/09 20:39:13', 'set ENABLE_BREAK')]}, 
        {'isn': '2260813003933', 'isn_data': [('620886', '(QSFC38)', '08/08 17:36:48', 'combo show')]}, 
        {'isn': '2260813000444', 'isn_data': [('620886', '(QSFC38)', '08/08 17:31:27', 'combo show')]}, 
        {'isn': '2260813002632', 'isn_data': [('991048', '(QSFCG4)', '08/08 20:26:26', 'DUT Bootloader Reset TIME OUT')]}, 
        {'isn': '2259346000525', 'isn_data': [('991952', '(QSFT15)', '08/10 22:18:48', 'IOS Ping Check')]}, 
        {'isn': '2260813003843', 'isn_data': [('620886', '(QSFC38)', '08/08 17:49:01', 'combo show')]}, 
        {'isn': '2260813000511', 'isn_data': [('620893', '(QSFT27)', '08/08 10:22:27', 'ControlBoard Hook Power ON')]}, 
        {'isn': '2259346000997', 'isn_data': [('991072', '(QSFCG4)', '08/10 08:02:36', 'DUT Reload TIME OUT')]}, 
        {'isn': '2260813003870', 'isn_data': [('991982', '(QSFT15)', '08/09 20:39:17', 'Press Enter')]}, 
        {'isn': '2260813003298', 'isn_data': [('995589', '(QSFI37)', '08/08 09:45:46', 'Battery 3V3 Test')]}, 
        {'isn': '2260813002775', 'isn_data': [('991034', '(QSFT15)', '08/09 13:03:02', 'Archive IOS')]}, 
        {'isn': '2259346000477', 'isn_data': [('620893', '(Q0FT18)', '08/10 05:10:35', 'DUT Timeout')]}, 
        {'isn': '2260813003115', 'isn_data': [('991982', '(QSFCG4)', '08/09 18:19:25', 'IOS Boot Up')]}, 
        {'isn': '2260813003174', 'isn_data': [('991036', '(QSFT15)', '08/09 19:35:19', 'IOS Back to Switch# Mode')]}, 
        {'isn': '2260813003670', 'isn_data': [('991053', '(QSFCG4)', '08/09 03:48:09', 'DUT Bootloader Reset TIME OUT')]}, 
        {'isn': '2259346000439', 'isn_data': [('620841', '(QSFT15)', '08/10 03:36:36', 'DUT Turn On')]}, 
        {'isn': '2259346000375', 'isn_data': [('991048', '(QSFT33)', '08/10 06:40:57', 'Copy Flash File to BS')]}, 
        {'isn': '2260813002246', 'isn_data': [('991952', '(QSFF69)', '08/09 23:05:30', 'Boot Loader Check Version')]},
         {'isn': '2260813002547', 'isn_data': [('991034', '(QSFCG4)', '08/09 14:53:28', 'DUT Bootloader Reset TIME OUT')]}, 
         {'isn': '2260813003410', 'isn_data': [('991952', '(QSFT33)', '08/09 16:04:41', 'Copy Flash File to BS')]}, 
         {'isn': '2260813003860', 'isn_data': [('991982', '(QSFCG4)', '08/09 07:29:44', 'DUT Bootloader Reset TIME OUT')]}, 
         {'isn': '2260813003861', 'isn_data': [('995596', '(QSFC09)', '08/09 13:37:32', 'Loopback Test-SFP 1G Link TEST')]}, 
         {'isn': '2260813004022', 'isn_data': [('991034', '(QSFF69)', '08/09 09:23:44', 'Boot Loader Check Version')]}, 
         {'isn': '2260813001880', 'isn_data': [('620886', '(QSFT27)', '08/09 14:36:53', 'ControlBoard Hook Power ON')]}, 
         {'isn': '2259346000925', 'isn_data': [('620834', '(QSFF11)', '08/10 01:26:00', 'Pegatron MFG Version')]}, 
         {'isn': '2260813003378', 'isn_data': [('991043', '(QSFCG4)', '08/08 18:30:41', 'DUT Bootloader Reset TIME OUT')]}, 
         {'isn': '2260813003673', 'isn_data': [('620893', '(QSFT15)', '08/08 12:04:35', 'BurnIn Check')]}, 
         {'isn': '2259346000769', 'isn_data': [('620834', '(QSFF11)', '08/10 01:21:52', 'Pegatron MFG Version')]}, 
         {'isn': '2259346000744', 'isn_data': [('991036', '(QSFCG4)', '08/10 08:02:37', 'DUT Reload TIME OUT')]}, 
         {'isn': '2260813002695', 'isn_data': [('991951', '(QSFCG4)', '08/09 16:21:03', 'IOS Boot Up')]}, 
         {'isn': '2259346000599', 'isn_data': [('995548', '(QSFC09)', '08/09 17:24:24', 'Loopback Test-SFP 1G Link TEST')]}, 
         {'isn': '2259943802701', 'isn_data': [('995547', '(QSFCG4)', '08/10 23:40:26', 'Boot Up')]}, 
         {'isn': '2260813002370', 'isn_data': [('620835', '(QSFT15)', '08/08 15:43:11', 'DUT Turn On')]}, 
         {'isn': '2259346000237', 'isn_data': [('995548', '(QSFC09)', '08/09 17:19:45', 'Loopback Test-SFP 1G Link TEST')]}, 
         {'isn': '2260813001882', 'isn_data': [('991036', '(QSFCG4)', '08/09 12:11:20', 'IOS Boot Up')]}, 
         {'isn': '2260813003737', 'isn_data': [('620886', '(QSFC38)', '08/08 15:38:06', 'Combo copper-prefer setup')]}, 
         {'isn': '2259346000517', 'isn_data': [('995547', '(QSFL06)', '08/09 19:00:06', 'Check Green LED Color')]}, 
         {'isn': '2260813002769', 'isn_data': [('991033', '(QSFCG4)', '08/09 18:56:15', 'DUT Reload TIME OUT')]}, 
         {'isn': '2259346000495', 'isn_data': [('620893', '(QSFC35)', '08/10 04:02:57', 'Port 0/0 LinkUP')]}, 
         {'isn': '2260813003506', 'isn_data': [('991042', '(QSFCG4)', '08/09 17:37:32', 'IOS Boot Up')]}, 
         {'isn': '2260813002783', 'isn_data': [('991943', '(QSFT33)', '08/09 11:49:54', 'Copy Flash File to BS')]}]}



def get_now_daytime():
    now = datetime.datetime.now()
    nowdatetime = now.strftime('%Y-%m-%d %H-%M')
    return nowdatetime


def clear_folder(folder_path):
    file_list = glob(f"{folder_path}\*")
    if len(file_list):
        for file in file_list:
            os.remove(file)

def create_today_download_file():
    nowdatetime = get_now_daytime()
    today_download_file = f"{nowdatetime} {execute_data['user_select_project']}"
    today_download_path = fr"{upper_folder_path}\IPLAS_Download\{today_download_file}"
    os.makedirs(today_download_path, exist_ok=True)
    return today_download_path

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

#將所有ISN合併成一個大list
def get_all_isn_list(data):
    fail_isn_list = []
    retest_isn_list = []
    for station, num in data.items():
        if num.get('fail_list'):
            fail_isn_list.extend(num.get('fail_list'))
        if num.get('retest_list'):
            retest_isn_list.extend(num.get('retest_list'))
    fail_isn_list = tuple(set(fail_isn_list))
    retest_isn_list = tuple(set(retest_isn_list))
    return fail_isn_list, retest_isn_list

#region 移動檔案和解壓縮
def move_zip_isn_file(today_download_path, data, pass_or_fail):
    zip_file_list = glob(f"{IPLAS_download_buffer}\*.zip")  #得到zip檔案列表
    for isn_file_data in data[:]:
        isn = isn_file_data['isn']  
        isn_datas = isn_file_data['isn_data']  #得到isn_data ex:('991982', '(QSFCG4)', '08/09 18:19:25', 'IOS Boot Up') 
        for isn_data in isn_datas[:]:
            file_time = re.sub("[/:]", "_", isn_data[2]) #將isn_data裡面的時間那欄(2)中出現的'/'和':'以'_'換掉
            file_name_pattern = re.compile(rf"{execute_data['user_select_project']}_(.*)_({isn_data[0]}(-[0-9])*_\d\d\d\d_{file_time})", re.I)
            for file_path in zip_file_list:
                find_file = file_name_pattern.findall(file_path)
                if len(find_file):
                    unzip_zip_file_and_move(file_path, today_download_path, find_file, pass_or_fail, isn_data, isn)
                    isn_datas.remove(isn_data)
                    if not len(isn_datas):
                        data.remove(isn_file_data)
                    break
    return data

def unzip_zip_file_and_move(file_path, today_download_path, find_file, pass_or_fail, isn_data, isn):
    upper_path = "\\".join(file_path.split("\\")[:-1])
    test_item = re.sub("[/: \\*?<>|-]", "_", isn_data[-1])
    test_station = find_file[0][0]
    time = find_file[0][1]
    unzip_file_folder = f"{isn}_{time}"
    move_to_file_path = f"{today_download_path}\{test_station}\{pass_or_fail}\{test_item}"
    if not os.path.isdir(move_to_file_path):                        
        os.makedirs(move_to_file_path) 
    Download_logger.debug(f"create file [{move_to_file_path}]")                     
    with ZipFile(file_path, 'r') as zip:                               #先解壓縮到原下載資料夾
        zip.extractall(f"{upper_path}\{unzip_file_folder}")
    Download_logger.debug(f"unzip zip file [{file_path}] -> [{upper_path}\{unzip_file_folder}]")
    csv_file_list = glob(f"{upper_path}\{unzip_file_folder}\*.csv")    #csv檔案重新命名，以免黨名太常打不開
    new_csv_file_name = csv_file_list[0].split("\\")[-1]    #csv檔案重新命名，以免黨名太常打不開
    new_csv_file_name =new_csv_file_name[:new_csv_file_name.index(test_station)-1]  #csv檔案重新命名，以免黨名太常打不開
    os.rename(csv_file_list[0], f"{upper_path}\{unzip_file_folder}\{new_csv_file_name}.csv")  #csv檔案重新命名，以免黨名太常打不開
    shutil.move(f"{upper_path}\{unzip_file_folder}", move_to_file_path) #解壓縮資料夾從預設下載地移到今天IPLAS下載位置
    Download_logger.debug(f"moeve file [{upper_path}\{unzip_file_folder}] -> [{move_to_file_path}]")
    os.remove(file_path)    

def move_csv_isn_file(today_download_path, data, pass_or_fail):
    csv_file_list = glob(f"{IPLAS_download_buffer}\*.csv")          
    if len(data) and len(csv_file_list):
        for isn_file_data in data[:]:
            isn = isn_file_data['isn']
            isn_datas = isn_file_data['isn_data']
            for isn_data in isn_datas[:]:
                file_time = re.sub("[/:]", "", isn_data[2])
                file_time = re.sub("[ ]", "_", file_time)
                file_name_pattern = re.compile(rf"{isn}_(.*)_{isn_data[0]}(-[0-9])*_(\w+)_(\w+){file_time}", re.I)
                for file_path in csv_file_list:
                    find_file = file_name_pattern.findall(file_path)
                    if len(find_file):
                        move_csv_file(file_path, today_download_path, find_file, pass_or_fail, isn_data, isn)
                        isn_datas.remove(isn_data)
                        if not len(isn_datas):
                            data.remove(isn_file_data)
                        break
    return data

def move_csv_file(file_path, today_download_path, find_file, pass_or_fail, isn_data, isn):
    test_station = find_file[0][0].split('_')[-1]
    test_item = re.sub("[/: \\*?<>|-]", "_", isn_data[-1])
    test_time = f"{find_file[0][-1]}_{re.sub('[/:]', '_', isn_data[2])}"
    file_folder = f"{isn}_{isn_data[0]}_{test_time}"
    move_to_file_path = f"{today_download_path}\{test_station}\{pass_or_fail}\{test_item}\{file_folder}"
    if not os.path.isdir(move_to_file_path):                        
        os.makedirs(move_to_file_path)
    Download_logger.debug(f"create file [{move_to_file_path}]")  
    new_csv_file_name = file_path.split("\\")[-1]
    new_csv_file_name = new_csv_file_name[:new_csv_file_name.index(test_station)-1]
    now_path = f"{IPLAS_download_buffer}\{new_csv_file_name}.csv"
    os.rename(file_path, now_path)
    shutil.move(now_path, move_to_file_path)
    Download_logger.debug(f"move csv file [{now_path}] -> [{move_to_file_path}]")  
#endregion

def move_and_unzip_isn_file(today_download_path, pass_fail_data_dic):
    error_list = []
    for pf, data in pass_fail_data_dic.items():
        data = move_zip_isn_file(today_download_path, data, pf.split('_')[0])
        data = move_csv_isn_file(today_download_path, data, pf.split('_')[0])
        if len(data):
            error_list.append(data)

    file_list = glob(f"{IPLAS_download_buffer}\*") 
    if len(error_list) and not len(file_list):
        print(data)
        print('有檔案未下載到')
    
    elif not len(error_list) and len(file_list):
        print(file_list)
        print('偵測到多餘檔案')
    
    elif len(error_list) and len(file_list):
        print(error_list)
        print(file_list)
        print('偵測到多餘檔案和未下載資料')

    elif not len(error_list) and not len(file_list):
        print("執行完成")

#用來顯示花費時間
def timer_and_debug(func):
    def warp():
        start_time = time.time()
        try:
            func()
        except Exception as ex:
            print(ex)
            return 0  
        finally:
            end_time = time.time()
            print(f'cost time {end_time-start_time}')
    return warp

@timer_and_debug
def main():
        clear_folder(IPLAS_download_buffer)  #清除download buffer裡面的檔案
        #today_download_path = r'D:\Qian\python\GIT\Tool\IPAS_download\main_program\IPLAS_Download\2022-08-05_10-47 SWITCH_CISCO_EZ1KA1'
        today_download_path = create_today_download_file()  #建立以'月-日 小時-分鐘_下載project' 為名子的資料夾
        pass_fail_data_dic = Start_Thread_main()
        if pass_fail_data_dic:
            move_and_unzip_isn_file(today_download_path, pass_fail_data_dic)
        print(iplas_data)

def Start_Thread_main():
    global iplas_data
    with ThreadPoolExecutor(max_workers=3) as executor:
        station_data = Get_Station_Data(executor)
        if check_station_data(station_data):
            station_data = Get_PassFail_ISN(executor, station_data)
            #print(station_data)
            pass_fail_data_dic = Download_ISN_File(executor, station_data)
            return pass_fail_data_dic
        else:
            print('此時間段沒數據')
                
    for driver in driver_data:  #關掉driver
        driver.close()
    

def Get_Station_Data(executor):
    '''
    去拿取個測站名稱以及pass/fail個數
    '''
    global iplas_data
    futures = [executor.submit(Login_Flow, ) for i in range(3)]   #三個瀏覽器登入
    futures = executor.submit(Get_Station_Data_Flow, )  #其中一個去拿測站的資訊
    iplas_data = futures.result()  #傳回測站的名子和pass fail個數
    station_data = deepcopy(iplas_data['station_data'])
    return station_data

def Get_PassFail_ISN(executor, station_data):
    '''
    拿取各測站fail中所有的測項中fail/retest個數以及ISN名單
    '''
    tmp_dic = {}
    station_list = [key for key in station_data.keys() if station_data[key]['fail_num']]     #傳入有fail數目的測站
    datas = [executor.submit(Get_PassFail_ISN_Flow, station) for station in station_list]    #得到各測站fail的isn名單
    for data in datas:   
        tmp_dic.update(data.result())
    station_data = dict_of_dict_merge(station_data, tmp_dic)
    return station_data

def Download_ISN_File(executor, station_data):
    '''
    傳入isn來獲取各isn裡面的所有資料以及下載檔案
    '''
    pass_fail_data_dic = {'fail_isn' : [], 'retest_isn_list' : []}
    fail_isn_list, retest_isn_list = get_all_isn_list(station_data)   #得到retest跟fail的isn名單
    
    isn_data = [executor.submit(Download_ISN_File_Flow, isn) for isn in retest_isn_list]   #下載retest isn列表裡的檔案
    for d in isn_data:
        pass_fail_data_dic['retest_isn_list'].append(d.result())

    ''' isn_data = [executor.submit(Download_ISN_File_Flow, isn) for isn in fail_isn_list]   #下載fil isn列表裡的檔案
    for d in isn_data:
        pass_fail_data_dic['fail_isn'].append(d.result()) '''
    return pass_fail_data_dic

#('995548', '(QSFC09)', '08/15 21:47:08', 'Loopback Test-SFP 1G Link TEST')
def Login_Flow():
    IPLAS = get_IPLAS()
    IPLAS.Login_IPLAS(main_data['userdata'])

def Get_Station_Data_Flow():
    IPLAS = get_IPLAS()
    IPLAS.Get_User_Project()
    IPLAS.Jump_to_Project_page(execute_data['user_select_project'])
    IPLAS.Get_Time_Option()
    IPLAS.Choose_Time(execute_data['time_selection'])
    IPLAS.Get_Necessary_Parameter()
    IPLAS.Get_Stationname_and_PassFail()
    return IPLAS.iplas_data

def Get_PassFail_ISN_Flow(station):
    IPLAS = get_IPLAS()
    IPLAS.Get_PassFail_ISN(station, execute_data['user_select_project'], iplas_data['queryid'])
    return IPLAS.iplas_data

def Download_ISN_File_Flow(isn):
    IPLAS = get_IPLAS()
    IPLAS.Download_ISN_File(execute_data['user_select_project'], isn)
    return IPLAS.iplas_data





def _test():
    #today_download_path = r'D:\Qian\2022-08-05_10-47 SWITCH_CISCO_EZ1KA1'

    #move_and_unzip_isn_file(today_download_path, data)
    driver = set_chrome_driver()
    driver_data[driver] = 1
    IPLAS = IPLAS_Flow(driver, Download_logger, driver_data)
    IPLAS.Login_IPLAS(main_data['userdata'])
    IPLAS.Download_ISN_File(execute_data['user_select_project'], isn = '2259943802782')
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
   



if __name__ == "__main__":
    main()
    #_test()

