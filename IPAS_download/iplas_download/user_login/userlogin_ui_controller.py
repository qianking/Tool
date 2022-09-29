import getpass
from login_ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox  
import requests
from requests_ntlm import HttpNtlmAuth
import lib.crypt as crypt

class MainWindow_contriller(QMainWindow):
    def __init__(self, user_data_path):
        super(MainWindow_contriller, self).__init__()
        self.userdata = []
        self.user_data_path = user_data_path
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_user_name()
        self.set_description_text()
        self.login_btm()

    def set_description_text(self):
        self.ui.label.setText('第一次使用或是密碼有改變時請輸入OA密碼')
    
    def write_in_data(self):
        self.userdata.append(self.ui.password_input.text())
        self.check_user_data()
    
    def set_user_name(self):
        self.user_name = getpass.getuser()
        self.userdata.append(self.user_name)
        self.ui.user_input.setText(self.user_name)
        

    def login_btm(self):
        self.ui.login_btm.clicked.connect(self.write_in_data)
        

    def password_error_msg(self):
        QMessageBox.warning(self, 'warning', 'Wrong Userdata!', QMessageBox.Ok)
        self.ui.user_input.clear()
        self.ui.password_input.clear()


    def login_msg(self):
        QMessageBox.information(self, 'login info', 'Login Success!', QMessageBox.Ok)
        self.close()
    
    def password_change_msg(self):
        QMessageBox.information(self, 'info', 'Find Password Changed', QMessageBox.Ok)
    
    def internet_error_msg(self):
        QMessageBox.critical(self, 'error', 'Internet ERROR', QMessageBox.Ok)
    

    def check_user_data(self):
        if len(self.userdata):
            code = self.checkpass_request(self.userdata)
            if code == 401:
                self.password_error_msg() 
                del self.userdata[:]
            if code == 200:
                data = ' '.join(self.userdata)
                en_data = crypt.Encrypt(data)
                with open(self.user_data_path, 'wb') as f:
                    f.write(en_data)
                self.login_msg()
        else:
            QMessageBox.warning(self, 'warning', 'Please Enter OA Password', QMessageBox.Ok)   


    def checkpass_request(self, data):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        proxies = {"http":"proxy8.intra:80"}
        auth = HttpNtlmAuth(data[0], data[1])
        url = 'http://eip.tw.pegatroncorp.com/'
        try:
            resp = requests.get(url = url,headers = headers, proxies=proxies, auth = auth, timeout=300)
        except Exception as ex:
            self.internet_error_msg()
            print('登入驗證錯誤 error : ', ex)
            self.close()
            return 11001
        else:
            return resp.status_code  

if __name__ == "__main__":
    data = ['Andy_Chien', 'Qianking0706']

    '''
    正常status_code為200
    帳密資訊有錯為401(驗證錯誤)

    '''
        




    

     

    
    
    
    
    

    

        

        