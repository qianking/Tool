import sys
import os
import lib.crypt as crypt
import userlogin_ui_controller as login
from PySide6.QtWidgets import QApplication

current_path = os.path.dirname(os.path.abspath(__file__))
upper_folder_path = '\\'.join(current_path.split('\\')[:-1])     #到上一層資料夾

user_data_folder = fr"{upper_folder_path}\docs"   #使用者帳密在上一層資料夾中的data資料夾中
os.makedirs(user_data_folder, exist_ok=True)
user_data_path = fr"{user_data_folder}\fw7ssv7b9bdb7ddn"   

def user_login_and_check_internet():
    userdata = []
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    login_window = login.MainWindow_contriller(user_data_path)  
    if (not os.path.exists(user_data_path)) or (os.path.getsize(user_data_path) == 0):
        login_window.show()
        app.exec()
        return login_window.userdata
    else:
        with open(user_data_path, 'rb') as f:
            b_userdata = f.readline()
        de_userdata = crypt.Decrypt(b_userdata)
        userdata = de_userdata.split(' ')
        code = login_window.checkpass_request(userdata)
        if code == 401:
            login_window.password_change_msg()
            login_window.show()
            app.exec()   
            return login_window.userdata 
        elif code == 200:
            return userdata
        elif code == 11001:
            return code

def return_user_data():
    userdata = user_login_and_check_internet()
    return userdata

if __name__ == "__main__":
    print(return_user_data())