import sys
import os
import time
import json
import traceback
from zipfile import ZipFile
from datetime import datetime
import requests
from requests_ntlm import HttpNtlmAuth
from win32com import client as wincom_client
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget, QWidget, QMainWindow, QLabel, QGridLayout

sys.path.append("./user_login")
sys.path.append("./user_login/lib")
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath( __file__ ))))
from userlogin_ui_controller import Login
import login_flow as login_flow
import _crypt
from IPLAS_Download import Get_User_Project
import lib.create_log as create_log
from Pre_proccess_controller import Pre_process


current_path = os.path.dirname(os.path.abspath(__file__))
upper_folder_path = '\\'.join(current_path.split('\\')[:-1])     #到上一層資料夾

docs_folder = fr"{upper_folder_path}\docs"   #使用者帳密在上一層資料夾中的data資料夾中
os.makedirs(docs_folder, exist_ok=True)
  
pre_proccess_log = fr"{upper_folder_path}\logs"
os.makedirs(pre_proccess_log, exist_ok=True)
pre_proccess_log = create_log.create_logger(fr"{pre_proccess_log}\pre_proccess.txt", 'pre_proccess_log')

ui_signal = None

class Login_and_Checkinternet():
    user_data_path = fr"{docs_folder}\fw7ssv7b9bdb7ddn" 

    def __init__(self, parent = None):
        #super(Login_and_Checkinternet, self).__init__(parent)
        self.ui_tool = UI_TOOL()

    def user_login_and_check_internet(self):
        pre_proccess_log.debug('Check user information')
        send_to_ui('status',txt = 'Check user information')
        if (not os.path.exists(self.user_data_path)) or (os.path.getsize(self.user_data_path) == 0):
            self.open_login_ui()
        return self.get_user_data()
        
    def get_user_data(self):
        userdata = list()
        with open(self.user_data_path, 'rb') as f:
            b_userdata = f.readline()
        de_userdata = _crypt.Decrypt(b_userdata)
        userdata = de_userdata.split(' ')

        pre_proccess_log.debug('Get user information')
        send_to_ui('status',txt = 'Get user information')
        code = login_flow._checkpass_request(userdata)
        if code == 404:
            pre_proccess_log.critical('Internet ERROR, please check your internet!')
            send_to_ui('status',txt = 'Internet ERROR, please check your internet!')

        while code == 404:
            time.sleep(5)
            code = login_flow._checkpass_request(userdata)
            
        if code == 401:
            pre_proccess_log.debug('find password change')
            
            self.ui_tool.password_change_box()
            userdata = self.open_login_ui() 
            if userdata:
                return userdata

        elif code == 200:
            pre_proccess_log.debug('Get user information successfully')
            return userdata

    def open_login_ui(self):
        ''' app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv) '''
        self.login = Login(self.user_data_path)
        self.login.show()
        return self.login.userdata


class Check_Chrome_Driver():
    chrome_driver_mapping_file = fr"{docs_folder}\mapping.json"
    chrome_driver_exe = fr"{docs_folder}\chromedriver.exe"
    chrome_driver_zip = fr"{docs_folder}\chromedriver_win32.zip"
    chrome_lastestdriverversion_url = "http://chromedriver.storage.googleapis.com"

    def __init__(self, userdata):
        self.ui_tool = UI_TOOL()
        self.user_data = userdata
        self.default_chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        self.proxies = {"http":"proxy8.intra:80"}
        self.auth = HttpNtlmAuth(self.user_data[0], self.user_data[1])

    @staticmethod
    def _write_json(file_path, info):
        with open(file_path, 'w') as f:
            json.dump(info, f, indent = 2)

    @staticmethod
    def _read_json(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def get_and_transfer_time(now = None):
        if not now:
            now = datetime.now()
            return now
        day = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        return day

    @staticmethod
    def get_file_version(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("{!r} file not found".format(file_path))
        wincom_job = wincom_client.Dispatch('Scripting.FileSystemObject')
        version = wincom_job.GetFileVersion(file_path)
        return version.strip()
    
    @staticmethod
    def unzip_driver_to_target_path(from_path, des_path):
        with ZipFile (from_path, 'r') as zip:
            zip.extractall(des_path)
    
    def get_chrome_driver_verion(self, chrome_path):
        if not chrome_path:
            if os.path.exists(self.default_chrome_path):
                chrome_path = self.default_chrome_path
            else:
                self.ui_tool.chrome_path_error_box()
                chrome_path = self.ui_tool.choose_chrome_path()
                pre_proccess_log.critical(f"Can't find chrome.exe path, choose path:{chrome_path}")
    
        chrome_version = self.get_file_version(chrome_path)
        chrome_major_ver = chrome_version.split(".")[0]
        pre_proccess_log.debug(f'get google chrome version:{chrome_major_ver}')
        return chrome_path, chrome_major_ver
    
    def last_driver_ver(self, chrome_major_ver):
        url = self.chrome_lastestdriverversion_url + f"/LATEST_RELEASE_{chrome_major_ver}"
        try:
            resp = requests.get(url = url,headers = self.headers, proxies = self.proxies, auth = self.auth, timeout=300, verify=False)

        except Exception as ex:
            ex_detail = get_exception_detail(ex)
            pre_proccess_log.critical(f'get chrome driver version exception: {ex_detail}')
            send_to_ui('error',txt = ex_detail)

        else:
            lastest_driver_ver = resp.text.strip()
            return lastest_driver_ver
    
    def download_driver(self, lastest_driver_version, des_folder):
        download_api = f"{self.chrome_lastestdriverversion_url}/{lastest_driver_version}/chromedriver_win32.zip"
        dest_path = os.path.join(des_folder, os.path.basename(download_api))
        
        try:
            resp = requests.get(url = download_api,headers = self.headers, proxies = self.proxies, auth = self.auth, timeout=300, verify=False)
        
        except Exception as ex:
            ex_detail = get_exception_detail(ex)
            pre_proccess_log.critical(f'download chrome driver exception: {ex_detail}')
            send_to_ui('error',txt = ex_detail)

        else:
            if resp.status_code == 200:
                with open(dest_path, 'wb') as f:
                    f.write(resp.content)
                pre_proccess_log.debug('download driver successfully')
            else:
                error_txt = f"unexpect error in [download_driver] get status.code:{resp.status_code}"
                pre_proccess_log.critical(error_txt)
                send_to_ui('error',txt = ex_detail)
      
    def read_driver_mapping(self):
        driver_mapping = {}
        if os.path.exists(self.chrome_driver_mapping_file):
            driver_mapping = self._read_json(self.chrome_driver_mapping_file)
        return driver_mapping.get('driver_data')
    
    
    def check_driver_available(self):
        send_to_ui('status',txt ='Check driver version')
        pre_proccess_log.debug('Check driver version')
        last_driver_version = 0
        
        now = self.get_and_transfer_time()
        driver_mapping = self.read_driver_mapping()

        
        last_check_time = driver_mapping['last_check_time'] if driver_mapping else None
        pre_proccess_log.debug(f"get last check time: {last_check_time}")
        last_check_time = self.get_and_transfer_time(last_check_time)
        chrome_path = driver_mapping['chrome_path'] if driver_mapping else None
        
        if (driver_mapping is None) or ((now-last_check_time).days >= 10):

            send_to_ui('status',txt = "Didn't find any driver, start install driver")
            pre_proccess_log.debug("Didn't find any driver, start install driver")

            chrome_path, chrome_major_ver = self.get_chrome_driver_verion(chrome_path)
            pre_proccess_log.debug(f"Get latest chrome version: {chrome_major_ver}")
            lastest_driver_ver = self.last_driver_ver(chrome_major_ver)
            pre_proccess_log.debug(f"Get latest driver version: {lastest_driver_ver}")

            last_check_time = str(now).split('.')[0]
            
            last_driver_version = driver_mapping['driver_version'] if driver_mapping else None
            pre_proccess_log.debug(f"Get last driver version: {last_driver_version}")

            if last_driver_version != lastest_driver_ver:
                send_to_ui('status',txt = "Start download driver")
                pre_proccess_log.debug("Start download driver")

                self.download_driver(lastest_driver_ver, docs_folder)
                self.unzip_driver_to_target_path(self.chrome_driver_zip, docs_folder)
                
            data = { 
                'driver_data' : {
                    "chrome_path" : chrome_path,
                    "chrome_major_ver" : chrome_major_ver,
                    "driver_path" : self.chrome_driver_exe,
                    "driver_version": lastest_driver_ver,
                    "last_check_time": last_check_time
                }
            }
            self._write_json(self.chrome_driver_mapping_file, data)

        return self.chrome_driver_exe

class Check_User_Project():
    def __init__(self, signal = None):
        self.signal = signal


class UI_TOOL():
    @staticmethod   
    def password_change_box():
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle('user info')
        MessageBox.setText('Find Password Changed')
        font = QFont("Arial", 12)
        MessageBox.setFont(font)
        MessageBox.show()
        app.exec()
    
    @staticmethod
    def chrome_path_error_box():
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle('Warning')
        MessageBox.setText("這台電腦的google chrome路徑不為預設路徑，請選擇正確的chrome.exe路徑，以完成後續的設定")
        font = QFont("Arial", 12)
        MessageBox.setFont(font)
        MessageBox.show()
        app.exec()
    
    @staticmethod
    def wrong_chrome_path_box():
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle('Warning')
        MessageBox.setText("請選擇正確的chrome.exe檔案")
        font = QFont("Arial", 12)
        MessageBox.setFont(font)
        MessageBox.show()
        app.exec()

   
    def choose_chrome_path(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        centralwidget = QWidget(MainWindow)
        label = QLabel(centralwidget)
        font = QFont("Arial", 12)
        label.setFont(font)

        label.setAlignment(Qt.AlignCenter)
        g_layout = QGridLayout(centralwidget)
        g_layout.addWidget(label, 0, 0, 0, 0)
        MainWindow.setCentralWidget(centralwidget)
        MainWindow.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        filename_choose, filetype = QFileDialog.getOpenFileName(MainWindow, 'Choose chrome path', 'C:/', "exe File (*exe)")
        if filename_choose.split('/')[-1] != "chrome.exe":
            self.wrong_chrome_path_box()
            self.choose_chrome_path()
        else:
            label.setText(f"選擇路徑:\n{filename_choose}\n (三秒後關閉)")
            QTimer.singleShot(3000, MainWindow.close)
            return filename_choose.replace("/", "\\")
        MainWindow.show()
        app.exec()


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

def send_to_ui(type, txt = None):
    if ui_signal:
        if type == 'status':
            ui_signal.status.emit(txt)
        if type == 'error':
            ui_signal.error.emit(txt)
        if type == 'finish':
            ui_signal.finish.emit()

def main_flow(signal = None):
    global ui_signal
    ui_signal = signal
    login = Login_and_Checkinternet()
    user_data = login.user_login_and_check_internet()
    print(user_data)
    driver = Check_Chrome_Driver(user_data)
    chrome_driver_exe = driver.check_driver_available()
    print(chrome_driver_exe)
    send_to_ui('finish')



if __name__ == "__main__":
    main_flow(None)
