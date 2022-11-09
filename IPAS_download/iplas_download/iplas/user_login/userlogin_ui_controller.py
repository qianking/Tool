import getpass
import sys
import time
from login_ui import Ui_MainWindow
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QLineEdit
from PySide6.QtCore import Signal, QRunnable, QThreadPool, QObject 
from PySide6.QtGui import QFont, QIcon, Qt
import login_flow


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.userdata = list()
        
        self._window = Ui_MainWindow()
        self._window.setupUi(self)
        
        self.keyPressEvent = self.PressReturnKey
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(3)
        self.font = QFont("KaiTi", 14)
        self.setup_ui()
    
    @property
    def window(self):
        return self._window

    def setup_ui(self):
        self.set_description_text()
        self.user_name_title()
        self.user_password_title()
        self.set_user_name()
        self.set_password_input()
        self.show_pwd_btm()
        self.set_login_btm()

    def set_description_text(self):
        self.description = self._window.label
        self.description.setFont(self.font)
        self.description.setText('第一次使用或密碼有改變時請輸入OA密碼')
    
    def user_name_title(self):
        self.username = self._window.username
        #self.username.setFont(self.font)
    
    def user_password_title(self):
        self.password = self._window.password
    
    def set_user_name(self):
        self.username_input = self._window.user_input
        self.user_name = getpass.getuser()
        font = QFont("Arial", 12)
        self.username_input.setFont(font)
        self.username_input.setText(self.user_name)
        self.username_input.setReadOnly(True)
    
    def set_password_input(self):
        self.password_input = self._window.password_input
        font = QFont("Arial", 12)
        self.password_input.setFont(font)
        self.password_input.setEchoMode(QLineEdit.Password)
    
    def show_pwd_btm(self):
        self.show_pwd = self._window.pushButton
        self.show_pwd.setText("")
        self.show_pwd.setStyleSheet("border-style: none")
        self.show_pwd.setIcon(QIcon(r'.\Icon\show-password.png'))
        self.show_pwd.clicked.connect(self.change_pwd_show_status)
    
    def change_pwd_show_status(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
        elif self.password_input.echoMode() == QLineEdit.EchoMode.Normal:
            self.password_input.setEchoMode(QLineEdit.Password)
        
    def PressReturnKey(self, event):
        if event.key() == Qt.Key_Return:
            self.check_userdata_and_write()
    
    def set_login_btm(self):
        self.login_btm = self._window.login_btm
        self.login_btm.clicked.connect(self.check_userdata_and_write)
    
    def check_userdata_and_write(self):
        if self.password_input.text():
            self.userdata.append(self.user_name)
            self.userdata.append(self.password_input.text())
            self.set_disable(True)
            self.start_thread()
        else:
            self.password_empty_error()
    
    def set_disable(self, bool):
        self.password_input.setDisabled(bool)
        self.show_pwd.setDisabled(bool)
        self.login_btm.setDisabled(bool)
       
    def event_proccess(self, event):
        self.internet_status = event
        
        if event == 401:
            self.userdata.clear()
            self.password_input.clear()
            self.password_error_msg()
        
        if event == 200:
            self.login_msg()
        
        if event == 404:
            self.internet_error_msg()

        self.set_disable(False)
        self.loading.end()
        self.description.setText('第一次使用或密碼有改變時請輸入OA密碼')
        

    def password_error_msg(self):
        QMessageBox.warning(self, 'warning', 'Wrong Userdata!', QMessageBox.Ok)
        
    def password_empty_error(self):
        QMessageBox.warning(self, 'warning', 'Please Enter OA Password', QMessageBox.Ok) 

    def login_msg(self):
        QMessageBox.information(self, 'login info', 'Login Success!', QMessageBox.Ok)
        self.close()
    
    def password_change_msg(self):
        QMessageBox.information(self, 'info', 'Find Password Changed', QMessageBox.Ok)
    
    def internet_error_msg(self):
        QMessageBox.critical(self, 'error', 'Internet ERROR, please check your internet!', QMessageBox.Ok)
    

    def start_thread(self):
        print(self.userdata)
        self.start_check_data = start_verify(self.user_data_path, self.userdata)
        self.start_check_data.signal.result.connect(self.event_proccess)
        self.threadpool.start(self.start_check_data)
        self.start_loading('Verify')
    
    def start_loading(self, txt):
        self.loading = Load_Thread(txt)
        self.loading.signal.loading.connect(self.load_label)
        self.threadpool.start(self.loading)

    def load_label(self, text):
        self.description.setText(text) 


class thread_signal(QObject):
    result = Signal(int)
    loading = Signal(str)

class start_verify(QRunnable):
    def __init__(self, user_data_path, userdata):
        super(start_verify, self).__init__()  
        self.signal = thread_signal()
        self.user_data_path = user_data_path
        self.userdata = userdata
        
    def run(self):
        login_flow.check_user_data(self.userdata, self.signal)


class Load_Thread(QRunnable):
    def __init__(self, txt):
        super(Load_Thread, self).__init__() 
        self.signal = thread_signal()
        self.flag = False
        self.txt = txt
        self.dot = ['.','..', '...']

    def run(self):
        while True :
            for i in self.dot:
                if self.flag:
                    break
                self.signal.loading.emit(f"{self.txt} {i}")
                time.sleep(1)
    
    def end(self):
        self.flag = True

if __name__ == "__main__":
    data = ['Andy_Chien', 'Qianking0706']

    '''
    正常status_code為200
    帳密資訊有錯為401(驗證錯誤)

    '''
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    mainwindow = Login()
    mainwindow.show()       
    sys.exit(app.exec())
        




    

     

    
    
    
    
    

    

        

        