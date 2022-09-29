from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
from copy import deepcopy
import traceback
import sys

class IPLAS_Flow():
    def __init__(self, driver, Download_logger, driver_data):
        self.driver_data = driver_data
        self.driver = driver
        self.Download_logger = Download_logger
        self.locl = 'SZ'
        self.IPLAS_URL_base = "http://cnsiplas.sz.pegatroncorp.com/iPLAS"
        self.iplas_data = {}  
                
    @staticmethod
    def find_isn_from_data(content):
        pattern = re.compile(r"_isn=(\w+)", re.I)      
        isn_list = pattern.findall(content)
        return isn_list


    @staticmethod
    def get_exception_detail(ex):
        error_class = ex.__class__.__name__ #取得錯誤類型
        detail = ex.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastcallstack = traceback.extract_tb(tb)[1]#取得Call Stack的最後一筆資料
        print(lastcallstack)
        fileName = lastcallstack[0] #取得發生的檔案名稱
        lineNum = lastcallstack[1] #取得發生的行號
        funcName = lastcallstack[2] #取得發生的函數名稱
        error_txt = f"[ERROR TYPE] {error_class}\n[ERROR DETAIL] {detail}\n[ERROR PATH] in file \"{fileName}\", line {lineNum}, function [{funcName}]"
        print(error_txt)
        return error_txt

    def _CustomLogger(func):
        def wrapper(self, *args, **kargs):
            try:
                logger_txt = func(self, *args, **kargs)    
                self.Download_logger.debug(logger_txt)
            except Exception as ex:
                error_txt = self.get_exception_detail(ex)
                self.Download_logger.debug(error_txt)
                raise Exception(error_txt)

        return wrapper
       

    @_CustomLogger
    def Login_IPLAS(self, userdata):
        """
        登入IPLAS網站
        """
        self.driver.get('http://cnsiplas.sz.pegatroncorp.com/iPLAS')
        input_data = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type = 'text']")))
        input_data.send_keys(userdata[0])
        self.driver.find_element(by=By.CSS_SELECTOR, value="input[type = 'password']").send_keys(userdata[1])
        self.driver.find_element(by=By.CSS_SELECTOR, value=".btn.btn-default.pega_login.ldaplogin").click()
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".container.pega_home_page")))

        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Login_IPLAS] :success login IPLAS"
        return logger_txt


    @_CustomLogger
    def Get_User_Project(self):
        """
        得到使用者所有的project列表
        """
        tmp_list = []
        project_list = self.driver.find_elements(by=By.CSS_SELECTOR, value="li[class^='js-prj']")
        for project in project_list:   
            tmp_list.append(project.get_attribute("innerText"))
        self.iplas_data['user_all_project'] = deepcopy(tmp_list)

        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Get_User_Project] :get user project {self.iplas_data['user_all_project']}"
        return logger_txt


    @_CustomLogger  
    def Jump_to_Project_page(self, user_select_project):
        """
        直接轉跳到project頁面(test station)
        """
        url = f"{self.IPLAS_URL_base}/plm/SZ/{user_select_project}?_source=TEST"  #直接轉跳到project區域
        self.driver.get(url) 

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#linefail_0_0, .export_lineviewreport")))  #等到右上角report下載按鈕或是下方不同line的資訊出現
        WebDriverWait(self.driver, 30).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))  #等到loading畫面消失

        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Jump_to_Project_page] : Jump into url : {url}"
        return logger_txt

    
    @_CustomLogger
    def Get_Time_Option(self):
        """
        得到所有的時間選項
        """
        tmp_list = []
        time_option_element = self.driver.execute_script("return document.getElementsByClassName('glyphicon glyphicon-ok')")   #定位到所有Date Quary裡面每個選項裡面的class glyphicon glyphicon-ok元素 
        for time_options in time_option_element: 
            time_option = time_options.find_element_by_xpath("..")    #返回上一層元素
            time_op = time_option.get_attribute("innerText")        
            tmp_list.append(time_op.strip())
        self.iplas_data['time_option'] = deepcopy(tmp_list)

        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Get_Time_Option] : get all time option {self.iplas_data['time_option']}"
        return logger_txt


    @_CustomLogger
    def Choose_Time(self, time_selection):
        """
        選擇時間
        """
        time_select = time_selection['time']    #time_selection':{'time':'This Week', 'time_period':['2022/07/25 08:00', '2022/08/05 08:00']}
        time_index = self.iplas_data['time_option'].index(time_select)
        
        javaScript = f"document.getElementsByClassName('glyphicon glyphicon-ok')[{time_index}].click();"  #使用javascript選擇時間
        self.driver.execute_script(javaScript)
        if time_select == 'Select Manually' and (time_select in self.iplas_data['time_option']):  #如果是自己選擇時間段
            javaScript = f"document.getElementsByClassName('form-control')[0].value = '{time_selection['time_period'][0]}';" #填入選擇的時間段(開始)
            self.driver.execute_script(javaScript)
            time.sleep(0.5)
            self.driver.find_element(by=By.CSS_SELECTOR, value="#chk_nowdate").click()
            javaScript = f"document.getElementsByClassName('form-control')[1].value = '{time_selection['time_period'][1]}';"  #填入選擇的時間段(結束)
            self.driver.execute_script(javaScript)
            self.driver.find_element(by=By.CSS_SELECTOR, value=".btn.btn-primary").click() 
        elif time_select not in self.iplas_data['time_option']:   #如果選項不在iplas已經有的時間段裡
            raise NameError('time select not in IPLAS time list')

        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-body")))  #等到下方個個line的table出現  
        WebDriverWait(self.driver, 120).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))) #等到loading畫面消失


        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Choose_Time] : choose time option {time_select}"
        if time_select == 'Select Manually':
            time_period = " ~ ".join(time_selection['time_period'])
            logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Choose_Time] : choose time period {time_period}"
        return logger_txt
       

    @_CustomLogger
    def Get_Necessary_Parameter(self):
        """
        得到這次網址裡必要資料
        """
        herf = self.driver.find_elements(by=By.CSS_SELECTOR, value=".progress.progressbar-passfail a[target='_blank']")  #定位到所有test station fail裡面的網址位子
        href_url = herf[0].get_attribute('href')
        pattern = re.compile(r'queryid=(.*)', re.I) #提取queryid
        queryid = pattern.findall(href_url)
        self.iplas_data['queryid'] = queryid[0]

        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Get_Necessary_Parameter] : get queryid : {self.iplas_data['queryid']}"
        return logger_txt

    @_CustomLogger
    def Get_Stationname_and_PassFail(self):
        """
        得到各測站名稱以及pass/fail的個數
        """
        self.iplas_data['station_data'] = {}
        page = self.driver.find_elements(by=By.CSS_SELECTOR, value=".fa.fa-circle")  #得到總共的test station的網頁頁數
        page_num = len(page)
        if page_num == 0:  #如果才一頁
            page_num = 1
        for page in range(page_num):
            stations=self.driver.find_elements(by=By.CSS_SELECTOR, value=".pega-station-icon.js-pega-station.keep_sidechart")  #定位到最上方那排test station icon  
            station_name_list = [name.get_attribute('innerText') for name in stations]                                                                       

            for i, station_name in enumerate(station_name_list):           #找到所有測站名稱以及pass/fail個數
                fail=self.driver.find_element(by=By.CSS_SELECTOR, value=f"#stfail_{str(i)}")  #找到fail的元素
                fail_num = fail.get_attribute('innerText')  #得到fail的個數
                pass_ = self.driver.find_element(by=By.CSS_SELECTOR, value=f"#stpass_{str(i)}") #找到pass的元素
                pass_num = pass_.get_attribute('innerText') #得到pass的個數
                station_name = re.sub('[ \/*?:<>|-]', '_', station_name) 
                fail_num = int(fail_num) if fail_num != '' else None
                pass_num= int(pass_num) if pass_num != '' else None
                self.iplas_data['station_data'][station_name] = {'fail_num' : fail_num, 'pass_num' : pass_num}

            if page != (page_num-1):
                self.driver.find_element(by=By.CSS_SELECTOR, value="#page_next").click()
                time.sleep(0.5)

        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Get_Stationname_and_PassFail] : get stationname and pass/fail num : {self.iplas_data['station_data']}"
        return logger_txt

    @_CustomLogger
    def Get_PassFail_ISN(self, station, user_select_project, queryid):
        """
        進入各測站fail網頁，得到所有各測項 fail/retest的個數和isn列表
        """
        self.iplas_data[station] = {'fail_list':[], 'retest_list':[]}
        Fail_report_url = f"{self.IPLAS_URL_base}/failreport/SZ/{user_select_project}/All/all/All/{station}?_source=TEST&_id=all&_queryid={queryid}"
        self.driver.get(Fail_report_url)

        Table = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#reactive-table-2")))  #等到直到下方table出現
        WebDriverWait(self.driver, 30).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))) #等到loading畫面消失
        
        retest_station_num = self.driver.find_element(by=By.CSS_SELECTOR, value=".rows-per-page-count").get_attribute('innerText')  #得到所有fail的測項個數
        self.driver.find_element(by=By.CSS_SELECTOR, value=".form-control").send_keys(3*Keys.BACKSPACE)     #對於輸入個數那邊按backspace(刪掉原本的數字)
        self.driver.find_element(by=By.CSS_SELECTOR, value=".form-control").send_keys(str(retest_station_num))   #fail_isn那個網頁全展開，輸入全部測項個數並且按enter
        self.driver.find_element(by=By.CSS_SELECTOR, value=".form-control").send_keys(Keys.ENTER)
        time.sleep(0.5)
        title_name = ['error_name', 'error_code', 'error_count', 'fail_num', 'retest_pass_num']  #table的最上面的標題順序和名稱
        isn_data = []
        rows = Table.find_elements(by=By.TAG_NAME, value="tr")  #定位到table裡每一列
        for row in rows[1:]: #第一列為標題名子
            tmp_dic = {}
            cols = row.find_elements(by=By.TAG_NAME, value="td") #定位到每列中的每一行
            for i, name in enumerate(title_name):
                tmp_dic[name] = cols[i].get_attribute('innerText').replace("\xa0", '').strip() #將每一行中的內容存起來
                if i == 3 or i == 4:  #如果為fail或是retest_pass那兩行
                    if int(tmp_dic[name]):
                        data = cols[i].get_attribute('innerHTML')
                        isn_list =self.find_isn_from_data(data)
                        if i == 3:
                            self.iplas_data[station]['fail_list'].extend(isn_list)
                        if i == 4:
                            self.iplas_data[station]['retest_list'].extend(isn_list)
            isn_data.append(deepcopy(tmp_dic))
        self.iplas_data[station]['ISN_data'] = isn_data

        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Get_PassFail_ISN] : get {station} retest/fail isn data: {isn_data}"
        return logger_txt
    
    @_CustomLogger
    def Download_ISN_File(self, user_select_project, isn):
        """
        去各個isn頁面下載ISN
        """
        isn_data = []
        isn_url = f"{self.IPLAS_URL_base}/isn_history/SZ/{user_select_project}?_isn={isn}"
        self.driver.get(isn_url)
        WebDriverWait(self.driver, 15).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))) #等到loading畫面消失
        inners = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dl_fa_sop"))) #等到每個fail框框裡面的error code那個class出現
        for inner in inners:
            if "rgb(255, 51, 51)" in inner.get_attribute("style"):  #當那個框框的error code為紅色字
                ouuer_block = inner.find_element_by_xpath("../..")  #回到上上層(那個框框的最上層div)
                download = ouuer_block.find_elements(by=By.CSS_SELECTOR, value=".fa.fa-cloud-download") #定位到那個框框的下載按鈕
                if len(download):  #如果有下載按鈕
                    data = ouuer_block.get_attribute("outerText")
                    data = [i.strip() for i in data.split('\n') if i.strip() != ''] #將那個fail file的所有資訊包括deviceid、error code、時間、test item存起來
                    isn_data.append(tuple(data)) 
                    self.driver.execute_script("arguments[0].click();", download[0]) #使用javascript按下載
                    
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".toast.toast-success")))  #直到成功下載那個畫面出現
        WebDriverWait(self.driver, 30).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content")))
        self.iplas_data = {'isn' : isn, 'isn_data' : isn_data} 

        logger_txt = f"[DRIVER {self.driver_data[self.driver]}] IN [Download_ISN_File] : download isn : {isn}, get isn data: {isn_data}"
        return logger_txt
    
    #@_CustomLogger
    def ReDownload_ISN(self, user_select_project):
        


        
        
        
        
    

        
        
        
    
    


