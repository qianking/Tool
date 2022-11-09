import sys
import os
import time
import lib._crypt as crypt
from userlogin_ui_controller import Login
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QFont
import login_flow

current_path = os.path.dirname(os.path.abspath(__file__))
upper_folder_path = '\\'.join(current_path.split('\\')[:-2])     #到上一層資料夾

user_data_folder = fr"{upper_folder_path}\docs"   #使用者帳密在上一層資料夾中的data資料夾中
os.makedirs(user_data_folder, exist_ok=True)
user_data_path = fr"{user_data_folder}\fw7ssv7b9bdb7ddn"   


class Login_and_Checkinternet():

    def read_and_get_userdata():
        userdata = list()
        with open(user_data_path, 'rb') as f:
            b_userdata = f.readline()
        de_userdata = crypt.Decrypt(b_userdata)
        userdata = de_userdata.split(' ')
        return userdata


    def user_login_and_check_internet():
        if os.path.exists(user_data_path):
            

        if (not os.path.exists(user_data_path)) or (os.path.getsize(user_data_path) == 0):
            open_login_ui()
        
    
    def get_user_data():
        
        code = login_flow.checkpass_request(userdata)
        while code == 404:
            time.sleep(5)
            code = login_flow.checkpass_request(userdata)
            
        if code == 401:
            password_change_box()
            userdata = open_login_ui() 
            if userdata:
                return userdata

        elif code == 200:
            return userdata
        

    def open_login_ui():
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        mainwindow = Login(user_data_path)
        mainwindow.show()
        app.exec()
        
    def password_change_box():
        app = QApplication(sys.argv)
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle('user info')
        MessageBox.setText('Find Password Changed')
        font = QFont("Arial", 12)
        MessageBox.setFont(font)
        MessageBox.show()
        app.exec()


if __name__ == "__main__":
    print(user_login_and_check_internet())