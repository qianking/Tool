import sys
import os
from .userlogin_ui_controller import Login
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QFont
from ..Global_Variable import SingleTon_Variable, get_exception_detail
from .login_lib.loginlib import checkpass_request, Decrypt



 
class Login_and_Checkinternet():

    G = SingleTon_Variable()

    def __init__(self):
        self.user_data_path = fr"{self.G.docs_folder}\{self.G.user_data_name}"
        self.logger = self.G.logger

    def user_login_and_check_internet(self):
        #self.ui_signal.send_status("Check user data")
        self.logger.debug("Check user data")
        if os.path.exists(self.user_data_path):
            userdata = self._read_and_get_userdata()
            code = checkpass_request(userdata)
            self.logger.debug(f"get request respones code [{code}]")
            if code == 401:
                self.logger.debug("user password change")
                self._password_change_box()
                self._open_login_ui()
            if code == 404:
                self.logger.debug("user internet error")
                pass
            if code == 200:
                self.G.user_password = userdata
                return userdata

        if (not os.path.exists(self.user_data_path)) or (os.path.getsize(self.user_data_path) == 0):
            self.logger.debug("user login")
            print("user login")
            self._open_login_ui()
            self.G.user_password = self._read_and_get_userdata()
            return self._read_and_get_userdata()


    def _read_and_get_userdata(self):
        userdata = list()
        with open(self.user_data_path, 'rb') as f:
            b_userdata = f.readline()
        de_userdata = Decrypt(b_userdata)
        userdata = de_userdata.split(' ')
        return userdata

        
    def _open_login_ui(self):
        if not self.G.app:
            app = QApplication(sys.argv)
        else:
            app = self.G.app
        mainwindow = Login(self.user_data_path)
        mainwindow.show()
        app.exec()
        
    def _password_change_box():
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle('user info')
        MessageBox.setText('Find Password Changed')
        font = QFont("Arial", 12)
        MessageBox.setFont(font)
        MessageBox.show()
        app.exec()







''' if __name__ == "__main__": '''
''' current_path = os.path.dirname(os.path.abspath(__file__))
upper_folder_path = '\\'.join(current_path.split('\\')[:-2])     #到上兩層資料夾

user_data_folder = fr"{upper_folder_path}\docs"   #使用者帳密在上一層資料夾中的data資料夾中
os.makedirs(user_data_folder, exist_ok=True)
user_data_path = fr"{user_data_folder}\fw7ssv7b9bdb7ddn"  

login = Login_and_Checkinternet(user_data_path)
print(login.user_login_and_check_internet()) '''    