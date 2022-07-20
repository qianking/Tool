import sys
sys.path.append(r"C:\littleTooldata\IPLAS\program\my lib")
import os
from login_ui_2 import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox  
import requests
from requests_ntlm import HttpNtlmAuth
import file_util
import encode
tool_path = r"C:\littleTooldata\user_data"
userdata_path = f"{tool_path}\\userdata.txt"

userdata = []

class MainWindow_contriller(QMainWindow):
    def __init__(self):
        super(MainWindow_contriller, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.click_button()

    
    def write_in_data(self):
        userdata.append(self.ui.lineEdit.text())
        userdata.append(self.ui.lineEdit_2.text())
        self.check_user_data()
        

    def click_button(self):
        self.ui.pushButton.clicked.connect(self.write_in_data)
        

    def error_box(self):
        QMessageBox.warning(self, 'error', 'userdata wrong!', QMessageBox.Ok)
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()


    def login_box(self):
        QMessageBox.information(self, 'login info', 'login success', QMessageBox.Ok)
        self.close()
    
    def change(self):
        QMessageBox.information(self, 'info', 'find password change', QMessageBox.Ok)
    

    def check_user_data(self):
        if len(userdata):
            code = self.checkpass_request(userdata)
            if code == 401:
                self.error_box() 
                del userdata[:]
            if code == 200:
                with open(userdata_path, 'w') as f:
                    for i in userdata:
                        a = encode.encode(i)
                        f.write(a + '\n')
                self.login_box()  



    def checkpass_request(self, get_password):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        proxies = {"http":"proxy8.intra:80"}
        auth = HttpNtlmAuth(get_password[0], get_password[1])
        url = 'http://eip.tw.pegatroncorp.com/'
        try:
            resp = requests.get(url = url,headers = headers, proxies=proxies, auth = auth, timeout=300)
        except Exception as ex:
            print('proxy認證錯誤，請檢查你的認證!')
            print('error : ', ex)
            return 404
        else:
            return resp.status_code 
        
def create_ini_file(tool_path):
    if not os.path.exists(tool_path):
        os.makedirs(tool_path)    


def user_login():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow_contriller()  
    create_ini_file(tool_path)
    if (not os.path.exists(userdata_path)) or (os.path.getsize(userdata_path) == 0):
        window.show()
        app.exec_()
    else:
        with open(userdata_path, 'r') as f:
            obj_list = f.readlines()
            for line in obj_list:
                line = line.strip()
                a = encode.decode(line)
                userdata.append(a)
        main = MainWindow_contriller()
        code = main.checkpass_request(userdata)
        if code == 404:
            pass
        if code == 401:
            main.change()
            window.show()
            app.exec_()
        
        
             

def return_user_data():
    user_login()
    return userdata
   
    
if __name__ == "__main__":
    print(return_user_data())
     

    
    
    
    
    

    

        

        