import sys
import os
now_dir = os.path.dirname(os.path.abspath(__file__))
mymodule_dir = '\\'.join(now_dir.split('\\')[:-1])
sys.path.append(mymodule_dir)
from Global_Variable import SingleTon_Variable, get_exception_detail
from lib.login_lib import checkpass_request, Decrypt
from userlogin_ui_controller import Login
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QFont

 
class Login_and_Checkinternet():

    G = SingleTon_Variable()

    def __init__(self):
        self.user_data_path = self.G.user_data_path
        self.ui_signal = self.G.ui_signal

    def user_login_and_check_internet(self):
        self.ui_signal.send_status("Check user data")
        if os.path.exists(self.user_data_path):
            userdata = self._read_and_get_userdata()
            code = checkpass_request(userdata)
            if code == 401:
                self._password_change_box()
                self._open_login_ui()
            if code == 404:
                pass
            if code == 200:
                self.G.user_password = userdata
                return userdata

        if (not os.path.exists(user_data_path)) or (os.path.getsize(user_data_path) == 0):
            self._open_login_ui()
            return self._read_and_get_userdata()


    def _read_and_get_userdata(self):
        userdata = list()
        with open(self.user_data_path, 'rb') as f:
            b_userdata = f.readline()
        de_userdata = Decrypt(b_userdata)
        userdata = de_userdata.split(' ')
        return userdata

    def _send_signal(self):
        if self.signal:
            pass

        
    def _open_login_ui(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        mainwindow = Login(self.user_data_path)
        mainwindow.show()
        app.exec()
        
    def _password_change_box():
        app = QApplication(sys.argv)
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle('user info')
        MessageBox.setText('Find Password Changed')
        font = QFont("Arial", 12)
        MessageBox.setFont(font)
        MessageBox.show()
        app.exec()


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    upper_folder_path = '\\'.join(current_path.split('\\')[:-2])     #到上兩層資料夾

    user_data_folder = fr"{upper_folder_path}\docs"   #使用者帳密在上一層資料夾中的data資料夾中
    os.makedirs(user_data_folder, exist_ok=True)
    user_data_path = fr"{user_data_folder}\fw7ssv7b9bdb7ddn"  

    login = Login_and_Checkinternet(user_data_path)
    print(login.user_login_and_check_internet())