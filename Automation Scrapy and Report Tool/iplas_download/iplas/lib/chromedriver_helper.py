import json
import os, sys
import requests
from ..Global_Variable import SingleTon_Variable, get_exception_detail
from zipfile import ZipFile
from requests_ntlm import HttpNtlmAuth
from datetime import datetime
from win32com import client as wincom_client
import pythoncom
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget, QWidget, QMainWindow, QLabel, QGridLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer


class Check_Chrome_Driver():

    G = SingleTon_Variable()

    def __init__(self):
        self.docs_folder = self.G.docs_folder
        self.chrome_lastestdriverversion_url = "http://chromedriver.storage.googleapis.com"
        self.chrome_driver_mapping_file = fr"{self.docs_folder}\mapping.json"
        self.chrome_driver_exe = fr"{self.docs_folder}\chromedriver.exe"
        self.chrome_driver_zip = fr"{self.docs_folder}\chromedriver_win32.zip"

        self.ui_signal = self.G.ui_signal
        self.logger = self.G.logger
        self.ui_tool = UI_TOOL()
        self.default_chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
        self.proxies = {"http":"proxy8.intra:80"}
        self.auth = HttpNtlmAuth(self.G.user_password[0], self.G.user_password[1])

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
        pythoncom.CoInitialize()
        wincom_job = wincom_client.Dispatch('Scripting.FileSystemObject')
        version = wincom_job.GetFileVersion(file_path)
        pythoncom.CoUninitialize()
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
                self.logger.critical(f"Can't find chrome.exe path, choose path:{chrome_path}")
    
        chrome_version = self.get_file_version(chrome_path)
        chrome_major_ver = chrome_version.split(".")[0]
        self.G.logger.debug(f'get google chrome version:{chrome_major_ver}')
        return chrome_path, chrome_major_ver
    
    def last_driver_ver(self, chrome_major_ver):
        url = self.chrome_lastestdriverversion_url + f"/LATEST_RELEASE_{chrome_major_ver}"
        try:
            resp = requests.get(url = url,headers = self.headers, proxies = self.proxies, auth = self.auth, timeout=300, verify=False)

        except Exception as ex:
            ex_detail = get_exception_detail(ex)
            self.logger.critical(f'get chrome driver version exception: {ex_detail}')
            self.ui_signal.send_error_box(ex_detail)

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
            self.logger.critical(f'download chrome driver exception: {ex_detail}')
            self.ui_signal.send_error_box(ex_detail)

        else:
            if resp.status_code == 200:
                with open(dest_path, 'wb') as f:
                    f.write(resp.content)
                self.logger.debug('download driver successfully')
            else:
                error_txt = f"unexpect error in [download_driver] get status.code:{resp.status_code}"
                self.logger.critical(error_txt)
                self.ui_signal.send_error_box(ex_detail)
      
    def read_driver_mapping(self):
        driver_mapping = {}
        if os.path.exists(self.chrome_driver_mapping_file):
            driver_mapping = self._read_json(self.chrome_driver_mapping_file)
        return driver_mapping.get('driver_data')
    
    
    def check_driver_available(self):
        self.ui_signal.send_status('Check driver version')
        self.logger.debug('Check driver version')
        last_driver_version = 0
        
        now = self.get_and_transfer_time()
        driver_mapping = self.read_driver_mapping()

        
        last_check_time = driver_mapping['last_check_time'] if driver_mapping else None
        self.logger.debug(f"get last check time: {last_check_time}")
        last_check_time = self.get_and_transfer_time(last_check_time)
        chrome_path = driver_mapping['chrome_path'] if driver_mapping else None
        
        if (driver_mapping is None) or ((now-last_check_time).days >= 10):

            self.ui_signal.send_status("Didn't find any driver, start install driver")
            self.logger.debug("Didn't find any driver, start install driver")

            chrome_path, chrome_major_ver = self.get_chrome_driver_verion(chrome_path)
            self.logger.debug(f"Get latest chrome version: {chrome_major_ver}")
            lastest_driver_ver = self.last_driver_ver(chrome_major_ver)
            self.logger.debug(f"Get latest driver version: {lastest_driver_ver}")

            last_check_time = str(now).split('.')[0]
            
            last_driver_version = driver_mapping['driver_version'] if driver_mapping else None
            self.logger.debug(f"Get last driver version: {last_driver_version}")

            if last_driver_version != lastest_driver_ver:
                self.ui_signal.send_status("Start download driver")
                self.logger.debug("Start download driver")

                self.download_driver(lastest_driver_ver, self.docs_folder)
                self.unzip_driver_to_target_path(self.chrome_driver_zip, self.docs_folder)
                
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

        
        self.G.chrome_driver_path = self.chrome_driver_exe
        return self.chrome_driver_exe




class UI_TOOL():
    
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




if __name__ == "__main__":
    
    print(_check_driver_available())
    