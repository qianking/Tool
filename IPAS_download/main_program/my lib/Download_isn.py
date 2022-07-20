from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PySide2.QtWidgets import  QApplication,QMainWindow, QMessageBox, QDialog, QLabel 
from PySide2.QtGui import QMovie, QFont
import sys
sys.path.append(r"C:\littleTooldata\IPLAS\program\my lib")
import Excel_barchart
import time
import re
import os
import datetime
from glob import glob
import shutil
from copy import deepcopy
from userlogin_UI import return_user_data
from zipfile import ZipFile
import chromedriver_helper
import file_util
import argparse
import requests
from requests_ntlm import HttpNtlmAuth
import math

    
password = return_user_data()
chromedriver_helper.check_driver_available()


local = 'SZ'
''' All_project = [
    "SWITCH_CISCO_EZ1KA1",
    "UC_POLY_MTR",
    "UC_UNIFY_CP700",
    "EZ1K_A2_ACT2",
    "SWITCH_YAMAHA_BLUES"
  ] '''
#User_select_project = ""
#Time_selection_index = 6
#Time_selection = ''
#Input_datetime = []
#Check_box_default = [1]
#File_download_path = r"C:\littleTooldata\IPLAS\Download"
IPLAS_defaultset_path = r"C:\littleTooldata\IPLAS\data\default.json"
IPLAS_download_buffer = r"C:\littleTooldata\IPLAS\Download\buffer"

class Form(QMainWindow):
    def __init__(self, text, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("info")
        self.setGeometry(500,500,250,100)
        self.info = text
        self.text = QLabel(self)
        font = QFont("Arial", 14, QFont.Bold)
        self.text.setFont(font)
        self.text.setGeometry(20,5,250,100)
        self.text.setText(self.info)

def check_internet():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    proxies = {"http":"proxy8.intra:80"}
    auth = HttpNtlmAuth(password[0], password[1])
    url = 'http://eip.tw.pegatroncorp.com/'
    try :
        resp = requests.get(url = url,headers = headers, proxies=proxies, auth = auth, timeout=300)
    except Exception:
        return False
    else:
        return True

def get_args_from_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-all', type = str, nargs='+')
    parser.add_argument('-pro', type = str, nargs='+')
    parser.add_argument('-time', type = str, nargs='+')
    parser.add_argument('-check', type = str, nargs='+')
    parser.add_argument('-path', type = str, nargs = 1)
    return parser
    

''' 去設定參數,假設參數是從cmd傳進來,那就代表是設定排程用的,那就從傳進來的引數中提取參數
假設有lwargs有參數傳進來,那就代表是使用者按執行,那就從使用者想要執行的參數來執行'''
def get_variable(**kwargs): 
    global All_project
    global User_select_project
    global Time_selection_index
    global Time_selection
    global Time_period
    global Input_datetime
    global Check_box_default
    global File_download_path
    
    '''execute_dict = {"All_project" : All_project,
                        "Select_project" : [project, index(project)],
                        "Time_set" :  [selecttime, index(self.selecttime), timeperiod],
                        "Check_box_default" :  check_box,
                        "Download_path" : download_path,
                        'Set_schedular_time' : temp_arrang
                        }'''

    #del All_project[:]
    Check_box_default = []
    #arrengment_args = ['位置檔名', all project]
    parser = get_args_from_cmd()
    args = parser.parse_args()
    if args.all != None:
        All_project = args.all
        User_select_project = args.pro[0]
        Time_selection = args.time[0].replace('_', " ")
        Time_selection_index = int(args.time[1])
        Time_period = args.time[2]
        Time_period = Time_period.replace('_',' ')
        Time_period = Time_period.replace('+','~')

        Check_box_default_temp = args.check
        for i in Check_box_default_temp:
            Check_box_default.append(int(i))
        File_download_path = args.path[0]
        #print(All_project,User_select_project, Time_selection, Check_box_default, File_download_path)
        
    if "execute_dict" in kwargs.keys():
        execute_dict = kwargs['execute_dict']
        
        All_project = execute_dict["All_project"]
        User_select_project = execute_dict["Select_project"][0]
        Time_selection = execute_dict["Time_set"][0]
        Time_selection_index = execute_dict["Time_set"][1]
        
        datetime = execute_dict["Time_set"][2]
        Input_datetime = [datetime.split(' ')[0].strip() + " " + datetime.split(' ')[1].strip(), datetime.split(' ')[-2].strip() + " " + datetime.split(' ')[-1].strip()]
        Time_period =  Input_datetime[0] + '~' +  Input_datetime[1]
        Check_box_default = execute_dict["Check_box_default"]
        File_download_path = execute_dict["Download_path"]
    
    #print(Time_period)
    return All_project

def print_status_argument(text, **kwargs):
    if "self" in kwargs.keys():
        self = kwargs['self']
        status = kwargs['status']
        self.status.emit(text)

def get_chrome_driver():
    global driver
    driver_path = chromedriver_helper.return_driver_path()
    s = Service(driver_path)
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  
    prefs = {"download.default_directory": IPLAS_download_buffer,
            "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option("prefs",prefs)
    options.add_argument("--headless")
    driver = webdriver.Chrome(service = s, options = options)
    wait = WebDriverWait(driver, 180)
    return driver, wait

def run(**kwargs):
    global Download_logger
    now = datetime.datetime.now()
    nowdatetime = now.strftime('%Y-%m-%d_%H-%M')
    
    create_file(IPLAS_download_buffer)
    All_project = get_variable(**kwargs)
    driver, wait = get_chrome_driver()
    
    today_excute_download_name = nowdatetime + " " + User_select_project
    today_excute_download_path = f"{File_download_path}\{today_excute_download_name}"
    
    create_file(today_excute_download_path)
    today_excute_download_data_path = f"{today_excute_download_path}\data.txt"
    IPLAS_log_path = "C:\littleTooldata\IPLAS\logs"
    Download_logger = file_util.create_logger(IPLAS_log_path, f'{today_excute_download_name}_log')
    text = "Get information..."
    print(text)
    print_status_argument(text, **kwargs)
    Download_logger.info(text)
    #region 寫入下載資訊
    with open(today_excute_download_data_path,'a+') as f:
        Download_time = now.strftime('%Y/%m/%d %H:%M:%S')
        
        if Check_box_default[1] == 1:
            Choose_Download_option = 'Retset_Pass'
        if Check_box_default[2] == 1:
            Choose_Download_option = 'Fail'
        if Check_box_default[1] == 1 and Check_box_default[2] == 1:
            Choose_Download_option = 'Retset_Pass / Fail '
        f.write(f"Download_time : {Download_time}\n\n\
All_project : {All_project}\n\n\
Select_project : {User_select_project}\n\n\
Time_selection: {Time_selection}\n\n\
Download_option_choose : {Choose_Download_option}\n\n\
File_download_path : {File_download_path}\n\n\
=========================================================================================================")
#endregion

    get_project = []
    Station_Data = {}
    Station_Data.clear()

    driver.get('http://cnsiplas.sz.pegatroncorp.com/iPLAS')
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type = 'text']")))
    element = driver.find_element(by=By.CSS_SELECTOR, value="input[type = 'text']").send_keys(password[0])
    element = driver.find_element(by=By.CSS_SELECTOR, value="input[type = 'password']").send_keys(password[1])
    element = driver.find_element(by=By.CSS_SELECTOR, value=".btn.btn-default.pega_login.ldaplogin").click()
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".container.pega_home_page")))
    links=driver.find_elements(by=By.CSS_SELECTOR, value="li[class^='js-prj']")    #得到使用者所擁有的project
    
    
    length=len(links)
    for j in range(length):   
        get_project.append(links[j].get_attribute("innerText"))
    Download_logger.info(f"Get_user_project : {get_project}")
    
    #region 如果偵測到使用者的project有更新，那就寫回default檔案
    if get_project != All_project:
        All_project = get_project
        execute_dict = file_util.read_json(IPLAS_defaultset_path)
        data = {'All_project' : All_project, 
                'Select_project' :  execute_dict["Select_project"],
                'Time_set' : execute_dict["Time_set"],
                'Check_box_default' : execute_dict["Check_box_default"],
                'Download_path' :  execute_dict["Download_path"],
                'Set_schedular_time' : execute_dict["Set_schedular_time"]
            }
        file_util.write_json(IPLAS_defaultset_path, data)

    #endregion

    url = f"http://cnsiplas.sz.pegatroncorp.com/iPLAS/plm/SZ/{User_select_project}?_source=TEST"  #直接轉跳到project區域
    driver.get(url)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-body"))) #等到直到下方個工站區域出現
    #time.sleep(0.5)
    element = wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))) #等到直到載入畫面消失
    time.sleep(2.5)
    #element =wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "._showStPass.blinkgreen")))

    #選擇時間
    if Time_selection_index == 6:     #使用月曆選擇日期                     
        javaScript = "document.getElementsByClassName('glyphicon glyphicon-ok')[6].click();"
        driver.execute_script(javaScript)
        javaScript = f"document.getElementsByClassName('form-control')[0].value = '{Input_datetime[0]}';" 
        driver.execute_script(javaScript)
        time.sleep(1)
        driver.find_element(by=By.CSS_SELECTOR, value="#chk_nowdate").click()
        javaScript = f"document.getElementsByClassName('form-control')[1].value = '{Input_datetime[1]}';" 
        driver.execute_script(javaScript)
        driver.find_element(by=By.CSS_SELECTOR, value=".btn.btn-primary").click()
    else:                   #選擇已經有的日期配方
        javaScript = "document.getElementsByClassName('glyphicon glyphicon-ok')["+ str(Time_selection_index) + "].click();"
        driver.execute_script(javaScript)
    
    #time.sleep(2)
    element =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-body"))) #等到直到下方個工站區域出現
    element =wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))) #等到直到載入畫面消失
    time.sleep(1)
    #element =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "._showLinePass")))
                                                     
    element = driver.find_elements(by=By.CSS_SELECTOR, value=".progress.progressbar-passfail a[target='_blank']")
    temp_queryid = element[0].get_attribute('href')
    try:
        Fail_report_queryid = temp_queryid[temp_queryid.index('queryid=') + len('queryid='):]   #得到網址所要用的必要資訊
        Download_logger.info(f"Get_queryid: {Fail_report_queryid}")
    except Exception:
        with open(today_excute_download_data_path,'a+') as f:
            f.write("No Data in this time selection")
        Download_logger.info("No Data in this time selection")
        text = 'No Data in this time selection'
        print(text)
        print_status_argument(text, **kwargs)
        driver.close()    
    else:
        page = driver.find_elements(by=By.CSS_SELECTOR, value=".fa.fa-circle")  #得到總共的test station的網頁頁數
        page_num = len(page)
        click_num = page_num
        station_num = 0
        
        if page_num == 0:
            page_num = 1
        for p in range(page_num):
            links=driver.find_elements(by=By.CSS_SELECTOR, value=".pega-station-icon.js-pega-station.keep_sidechart")  
            length=len(links)  #所有測站的個數

            for j in range(length):                    #找到所有測站名稱以及pass/fail個數
                station = links[j].get_attribute('id')
                fail_name = '#stfail_' +  str(j)
                fail=driver.find_element(by=By.CSS_SELECTOR, value=fail_name)  
                fail_num = fail.get_attribute('innerText')
                pass_name = '#stpass_' +  str(j)
                pass_ = driver.find_element(by=By.CSS_SELECTOR, value=pass_name)
                pass_num = pass_.get_attribute('innerText')
                Station_Data[station_num] = {station : fail_num + '/' + pass_num}
                station_num = station_num + 1

            click_num = click_num - 1
            if click_num > 0:
                try:
                    next_page=driver.find_element(by=By.CSS_SELECTOR, value="#page_next").click()
                except Exception as ex:
                    Download_logger.info("click next page failed")
            time.sleep(0.5)
            
        #print('station_name:', Station_Data)
    #region列印得到的fail/pass個數到終端機上
        frist_key= list(Station_Data[0].keys())[0]
        frist_value= list(Station_Data[0].values())[0]
        text = f"{frist_key}: {frist_value}\n"
        #print_status_argument(text, **kwargs)
        k = len(Station_Data)
        for i in range(1,k):
            for key, value in Station_Data[i].items():
                text = text + f"          {key}: {value}\n"
                #print_status_argument(text, **kwargs)
        print_status_argument(text, **kwargs)
    #endregion    

    #region 得到該測站裡面所有有retest pass 和 fail的ISN
        Retest_psss = {} 
        Fail = {}
        Pass_Fail_num = []
        temp_pass_isn_num = 0
        temp_fail_isn_num = 0
        max_len = []
        iligal_simbol = [' ', '/', '\\', '*', '?', ':', '<', '>', '|'] 

        for i in range(len(Station_Data)):
            Retest_psss.clear()
            Fail.clear()
            station = list(Station_Data[i].keys())[0]
            Station_Fail_num = list(Station_Data[i].values())[0].split('/')[0]  #得到該測站的fail個數
            Fail_report_url = f"http://cnsiplas.sz.pegatroncorp.com/iPLAS/failreport/SZ/{User_select_project}/All/all/All/{station}?_source=TEST&_id=all&_queryid={Fail_report_queryid}"
            max_len_passname = 0
            max_len_failname = 0
            if int(Station_Fail_num):
                driver.get(Fail_report_url)
                element =wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".page-number-count")))
                time.sleep(1)
                retest_station_num = driver.find_element(by=By.CSS_SELECTOR, value=".rows-per-page-count").get_attribute('innerText')
                element = driver.find_element(by=By.CSS_SELECTOR, value=".form-inline.form-group.rows-per-page input[class='form-control']").send_keys('1000')   #fail_isn那個網頁全展開
                element = driver.find_element(by=By.CSS_SELECTOR, value=".form-inline.form-group.rows-per-page input[class='form-control']").send_keys(Keys.ENTER)
                time.sleep(0.5)
                for j in range(1, int(retest_station_num)+1):
                    Retest_pass_num = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[5]").get_attribute('innerText') #得到重測次數
                    Fail_num = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[4]").get_attribute('innerText') #得到重測次數
                    if int(Retest_pass_num):    #如果有重測
                        error_name = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[1]").get_attribute('innerText') #得到該工站名稱
                        error_code = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[2]").get_attribute('innerHTML') #得到該工站的代碼
                        error_code = error_code.split('&')[0]
                        for simbol in iligal_simbol:
                            if simbol in error_name:
                                error_name = error_name.replace(simbol, '-')
                        error_name = f'{error_name} ({error_code})'     
                        link = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[5]/div/a").get_attribute('data-content')#得到所有重測的isn
                        temp_isn = get_isn(link)
                        
                        pass_NUM = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[5]").get_attribute('innerText')
                        temp_pass_isn_num  = temp_pass_isn_num  + int(pass_NUM)
                        temp_isn = temp_isn
                        Retest_psss[error_name] = deepcopy(temp_isn)
                        
                        if len(error_name) > max_len_passname:       #找出最長的字的長度(排版用)
                            max_len_passname = len(error_name)
                    
                    if int(Fail_num):           #如果有fail
                        error_name = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[1]").get_attribute('innerText') #得到該工站
                        error_code = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[2]").get_attribute('innerHTML') #得到該工站的代碼
                        error_code = error_code.split('&')[0]
                        for simbol in iligal_simbol:
                            if simbol in error_name:
                                error_name = error_name.replace(simbol, '-')
                        error_name = f'{error_name} ({error_code})'
                        link = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[4]/div/div/a").get_attribute('data-content')#得到所有重測的isn
                        temp_isn = get_isn(link)
                        fail_NUM = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[3]/div[2]/div/table/tbody/tr[" + str(j) + "]/td[4]").get_attribute('innerText')
                        temp_fail_isn_num  = temp_fail_isn_num  + int(fail_NUM)
                        Fail[error_name] = deepcopy(temp_isn)
                        
                        if len(error_name) > max_len_failname:       #找出最長的字的長度(排版用)
                            max_len_failname = len(error_name)
                
                Station_Data[i]['Retest_psss'] = deepcopy(Retest_psss)
                Station_Data[i]['Fail'] = deepcopy(Fail)
                temp = [deepcopy(max_len_passname), deepcopy(max_len_failname)]
                max_len.append(temp) 
                time.sleep(0.5) 
            else:
                temp = [0, 0]
                max_len.append(temp)
        Pass_Fail_num = [temp_pass_isn_num, temp_fail_isn_num]
        if Check_box_default[1] == 1:
            All_download_num = temp_pass_isn_num
        if Check_box_default[2] == 1:
            All_download_num = temp_fail_isn_num 
        if Check_box_default[1] == 1 and Check_box_default[2] == 1:
            All_download_num = temp_pass_isn_num + temp_fail_isn_num 

        Download_logger.info(f"Station_Data: {Station_Data}")
        #print('\n\nStation_Data: ', Station_Data)
        #print('\nmax_len: ', max_len)
        #print('\nPass_Fail_num: ', Pass_Fail_num)
        Download_logger.info(f"Pass_Fail_num: {Pass_Fail_num}")
    #region 將pass/fail的個數印到終端機上面
        text = f"Get: Pass_num: {Pass_Fail_num[0]}\n                  Fail_num: {Pass_Fail_num[1]}"
        print_status_argument(text, **kwargs)
    #endregion   
        print('Retest Pass number: ', Pass_Fail_num[0], '\nFail number: ',Pass_Fail_num[1])
        fast_time = (Pass_Fail_num[0]*4 + (Pass_Fail_num[1]*4*4) + 60)/60
        fast_time = math.ceil(fast_time)
        long_time = (Pass_Fail_num[0]*8 + (Pass_Fail_num[1]*4*8) + 60)/60
        long_time = math.ceil(long_time)
        if fast_time != long_time:
            print(f'It will take about {fast_time} min to {long_time} min (depend on internet speed)')
            text = f'It will take about {fast_time} min to {long_time} min\n         (depend on internet speed)'
        else:
            print(f'It will take about {fast_time} min (depend on internet speed)')
            text = f'It will take about {fast_time}\n         (depend on internet speed)'
        print_status_argument(text, **kwargs)
        print("Start download...")
        text = Excel_barchart.draw_on_excel(Station_Data, User_select_project, Time_period, today_excute_download_path)
        print_status_argument(text, **kwargs)
        print(text)
        download_isn(Station_Data, driver, wait, today_excute_download_path , max_len, All_download_num, **kwargs)
       

#endregion

def download_isn(Station_Data, driver, wait, today_excute_download_path, max_len, All_download_num, **kwargs):
    Download_num = 0
    befor_unzip_num = 0
    after_unzip_num = 0
    isn_info = {}
    retry_fail_list = []
    temp_fail_list = []
    percentage = ''
    today_excute_download_data_path = f"{today_excute_download_path}\data.txt"
    for ind in range(len(Station_Data)):
        Test_station = list(Station_Data[ind].keys())[0]
        fail_num = list(Station_Data[ind].values())[0].split('/')[0] 
        with open(today_excute_download_data_path,'a+') as f:
            f.write(f"\n{Test_station} : {list(Station_Data[ind].values())[0]}\n")

        if int(fail_num) != 0:
            for i in range(1,3):
                if Check_box_default[i] == 1:       #下載fail和pass檔案
                    Pass_or_Fail = list(Station_Data[ind].keys())[i]
                    
                    Download_logger.info(f"{Test_station} {Pass_or_Fail}:")
                    #print(f"Test_station:{Test_station}\n Pass_or_Fail:{Pass_or_Fail}\n")
                    isn_list = list(Station_Data[ind].values())[i]
                    with open(today_excute_download_data_path,'a+') as f:  #將下載列表寫入txt file
                        f.write(f"\t\t{Pass_or_Fail} :\n")

                    for name, isn in isn_list.items():
                        temp = []
                        Fail_station = name 
                        Download_isn_list = isn
                        space_num = max_len[ind][i-1] - len(Fail_station)
                        ta = " "*space_num
                        with open(today_excute_download_data_path,'a+') as f:      #將下載列表寫入txt file
                            f.write(f"\t\t\t{Fail_station} : {ta}{Download_isn_list}\n")
                        Download_logger.info(f"Fail_station: {Fail_station}")
                        #print("Fail_station: ", Fail_station)
                        
                        Download_project_file = f"{today_excute_download_path}\{Test_station}\{Pass_or_Fail}\{Fail_station}"  #下載好的檔案要移到的地方
                        create_file(Download_project_file)

                        Download_logger.info(f"isn_list: {Download_isn_list}")
                        #print('isn_list: ', Download_isn_list)

                        for isn_now in Download_isn_list:     #依照工單下載
                            error_num = 0
                            retry = 0
                            del temp[:]
                            Fail_station_isn = isn_now
                            Fail_station_url = f"http://cnsiplas.sz.pegatroncorp.com/iPLAS/isn_history/SZ/{User_select_project}?_isn={Fail_station_isn}"
                            driver.get(Fail_station_url)

                            while retry != 3:    #當有網頁載入有問題時(載入太慢)，會重複三次，三次還是失敗的話就先跳過這個並且記錄下來
                                try:
                                    element = wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))   #等到直到loading 畫面消失
                                    lines = driver.find_elements(by=By.CSS_SELECTOR, value=f"div[data-target$='{Test_station}'] .fa.fa-angle-double-up")
                                    
                                except Exception as ex:
                                    Download_logger.exception(ex)
                                    print(ex)
                                    driver.get(Fail_station_url)
                                    retry = retry +1
                                else:
                                    break
                            
                            if retry == 3:
                                temp = [isn_now, Download_project_file]
                                retry_fail_list.append(deepcopy(temp)) 
                                continue
                            else:
                                #print(lines, len(lines))
                                num_of_line = len(lines)
                                for line in lines:
                                    line.click()
                                for num_est in range(num_of_line):
                                    id = f'{num_est}_{Test_station}'
                                    get_sytle = driver.find_elements(by=By.CSS_SELECTOR, value=f"div[id='{id}'] .dl_fa_sop") #得到該下拉式選單的長度
                                    #print('len:', len(get_sytle))
                                    for num in range(len(get_sytle)):
                                        color = get_sytle[num].get_attribute("style")
                                        if "rgb(255, 51, 51)" in color:  #找到紅色字就下載
                                            info = driver.find_elements(by=By.CSS_SELECTOR, value=f"div[id='{id}'] .download")[num]  
                                            deviceid = info.get_attribute('deviceid')
                                            fail_time = info.get_attribute('time')
                                                                                        #儲存該工單的 deviceID, time,isn 用來比對下載後檔案對應的ISN是哪個
                                            change_symbol= ['/', ':']
                                            fail_time = fail_time.split('.')[0]
                                            for symbol in change_symbol:
                                                if symbol in fail_time:
                                                    fail_time = fail_time.replace(symbol, '_')
                                            temp = [isn_now, Download_project_file, id]
                                            isn_info[f"{deviceid}_{fail_time}"] = deepcopy(temp)
                                            try:
                                                download_click = driver.find_elements(by=By.CSS_SELECTOR, value=f"div[id='{id}'] .fa.fa-cloud-download") #點擊下載按鈕(cloude圖案)
                                                download_click[num].click()
                                                if i == 2:
                                                    wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))
                                                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".toast.toast-success")))
                                                #time.sleep(0.5)
                                            except Exception as ex:
                                                Download_logger.exception('list too long to click')
                                                error_num = error_num +1
                                                print(ex)
                                                continue
                            
                                download_success = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".toast.toast-success"))) 
                        
                        time.sleep(1)
                        Download_logger.info(f"Before moveing file: {isn_info}")
                        Download_logger.info(f"Retry times: {retry}")
                        if len(retry_fail_list) != 0:
                            Download_logger.info(f"Retry isn: {retry_fail_list}")
                        
                        befor_unzip_num = get_num_isn(isn_info)

                        #print('\nisn_info: ', isn_info, '\nretry:', retry)
                        unzip_and_move_file(Test_station, Download_project_file, isn_info)
                        
                        after_unzip_num = get_num_isn(isn_info)

                        #region 將下載進度列印到終端機上

                        if error_num  == 0:
                            Download_num = Download_num + (befor_unzip_num - after_unzip_num)   
                            #print(Download_num/All_download_num*100)
                            text = 'Processing : {:.0f}%'.format(Download_num/All_download_num*100)
                            if percentage != text:
                                print(text)
                                print_status_argument(text, **kwargs) 
                            percentage = text       
                        #endregion
                        
                        Download_logger.info(f"After moveing file: {isn_info}")
                        #print('\nisn_info: ', isn_info)
                        time.sleep(0.5)

    retry_fail_list = redownload_isn(driver, wait, isn_info, percentage, retry_fail_list, User_select_project, Download_num, All_download_num, **kwargs)
    


    #region將是否有下載失敗的資訊寫入data.txt
    with open(today_excute_download_data_path,'a+') as f:      
        f.write("=========================================================================================================")
        if len(retry_fail_list) == 0:
            f.write("\nDownload retry fail : None")
        else:
            f.write(f"\nDownload retry fail : {retry_fail_list}")
    #endregion 
    
    #region 將下載完成列印到終端機上
    if len(retry_fail_list) != 0:
        k = len(retry_fail_list)
        text = f'Have {str(k)} Download Failed!'
        print(text)
        print_status_argument(text, **kwargs) 
        driver.quit()
        time.sleep(600)
    else:
        text = 'Download completed'
        print(text)
        for file in glob(f"{IPLAS_download_buffer}\*.zip"):
            os.remove(file)
        print_status_argument(text, **kwargs) 
        driver.quit()    
    #endregion
    
       

def get_num_isn(isn_info):
    isn = []
    if len(isn_info) == 0:
        return 0
    else:
        temp_list = list(isn_info.values())
        for i in range(len(temp_list)):
            if temp_list[i][0] not in isn:
                isn.append(temp_list[i][0])
        return len(isn)

def unzip_and_move_file(Test_station, Download_project_file, isn_info):
    #改為偵測下載的檔名(符合的檔名)，不偵測下載的檔案類型
    #因為會有下載的檔案不一定為zip檔的問題
    for file in glob(f"{IPLAS_download_buffer}\*.zip"):
        file_name_pattern = r'(\d{6}(-[0-9])*\w+\s\w+)'
        file_name = re.search(file_name_pattern, file)
        file_name = file_name.group()
        try:
            Fail_station_isn = isn_info.pop(file_name)
        except:
            print(f"find unexpected file : {file}")
            continue
        else:
            Fail_station_isn = Fail_station_isn[0]
            file_name = file_name.replace('_', '-')
            file_name = f"{Fail_station_isn}_{Test_station}_{file_name}"
            Download_project_file_name =f"{Download_project_file}\{file_name}"
            try:
                with ZipFile(file, 'r') as zip:
                    zip.extractall(Download_project_file_name)
            except Exception as ex:
                shutil.rmtree(Download_project_file_name)
                with ZipFile(file, 'r') as zip:
                    zip.extractall(f"{File_download_path}\{file_name}")
                shutil.move(f"{File_download_path}\{file_name}",Download_project_file)
                os.remove(file)
            else:
                os.remove(file)

#清洗數據 尋找工單
def get_isn(link):         
    pattern = r'>(\w+)<'       
    temp_isn = re.findall(pattern,link)
    return temp_isn

def create_file(path):
    if not os.path.exists(path):
        os.makedirs(path)

#下載遺漏的ISN
def redownload_isn(driver, wait, isn_info, percentage, retry_fail_list, User_select_project, Download_num, All_download_num, **kwargs):
    #ISN: {'995596_2022_05_16 07_05_04': ['2222013601839', 'C:\\littleTooldata\\IPLAS\\Download\\2022-05-16_16-15 SWITCH_CISCO_EZ1KA1\\Pretest\\Fail\\USBCOM-Port-Open']}
    
    befor_unzip_num = 0
    after_unzip_num = 0
    retry = 0
    temp = []
    fail_list = []
    if len(isn_info) != 0:
        Download_logger.info(f"Start reDownload missing ISN: {isn_info}")
        print(f"Start reDownload missing ISN: {isn_info}")
        while len(isn_info) != 0:
            retry = 0
            del temp [:]
            #print(f'ISN: {isn_info}')
            time_search = list(isn_info.keys())[0]       #
            isn_path_list = list(isn_info.values())[0]
            path = isn_path_list[1]
            isn = isn_path_list[0]
            id = isn_path_list[2]
            test_sation = path.split('\\')[-3]
            pattern = r'_(\d{4}\w+\s\w+)'
            time_search_A = re.findall(pattern,time_search)
            time_search_A = time_search_A[0].split(' ')[0].replace('_', '/') + " " + time_search_A[0].split(' ')[1].replace('_', ':') + ".000"
            Fail_station_url = f"http://cnsiplas.sz.pegatroncorp.com/iPLAS/isn_history/SZ/{User_select_project}?_isn={isn}"
            Download_logger.info(f"get_fail_url: {Fail_station_url}")
            while retry != 3:
                try:
                    driver.get(Fail_station_url)
                    element = wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))   #等到直到loading 畫面消失
                    element = driver.find_element(by=By.CSS_SELECTOR, value=f"div[data-target='#{id}'] .fa.fa-angle-double-up").click()
                    download = driver.find_element(by=By.CSS_SELECTOR, value=f"a[time='{time_search_A}'] .fa.fa-cloud-download").click()
                except Exception as ex:
                    Download_logger.exception(ex)
                    print(ex)
                    retry = retry + 1 
                    time.sleep(0.5)
                else:
                    download_success = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".toast.toast-success")))
                    break
            if retry == 3:
                temp = isn_info.pop(time_search)
                retry_fail_list.append(deepcopy(temp)) 
                continue
                
            time.sleep(0.5)
                
            befor_unzip_num = get_num_isn(isn_info)
                
            unzip_and_move_file(test_sation, path, isn_info)
                
            after_unzip_num = get_num_isn(isn_info)
                
            #region 將進度印到終端機上面
            if after_unzip_num != befor_unzip_num:
                Download_num = Download_num + (befor_unzip_num - after_unzip_num)
                #print(Download_num/All_download_num*100)
                text = 'Processing : {:.0f}%'.format(Download_num/All_download_num*100)
                if percentage != text:
                    print(text)
                    print_status_argument(text, **kwargs) 
                percentage = text 
            #endregion 
            
            time.sleep(0.5)
    return retry_fail_list

def stop_download_file(**signal):
    if 'stop' in signal:
        driver.close()
        for file in glob(f"{IPLAS_download_buffer}\*.zip"):
            os.remove(file)

def start_downloading(**kwargs):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    if check_internet():
        print("Check internet: ok")
        run(**kwargs)
    else:
        window = Form('請檢查網路!')
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    start_downloading()
    #run()
    #download_isn()
    #redownload_isn()