import sys
import os
import time
import threading
from datetime import datetime
from PySide6.QtWidgets import QApplication
from iplas.Global_Variable import SingleTon_Variable, get_exception_detail
from iplas.user_login.User_Login import Login_and_Checkinternet
from iplas.lib.chromedriver_helper import Check_Chrome_Driver
from iplas.Status_show_controller import Pre_process
import iplas.lib.create_log as create_log

G = SingleTon_Variable()

current_path = os.path.dirname(os.path.abspath(__file__)) #這層位置

docs_folder = fr"{current_path}\docs"   #需要用到的資料放在這一層docs資料夾中
os.makedirs(docs_folder, exist_ok=True)
  
pre_proccess_log = fr"{current_path}\logs"  #下載的log檔放在這一層log資料夾中
os.makedirs(pre_proccess_log, exist_ok=True)
pre_proccess_log = create_log.create_logger(fr"{pre_proccess_log}\pre_proccess.txt", 'pre_proccess_log')

G.docs_folder = docs_folder
G.logger = pre_proccess_log


def main_flow():
    login = Login_and_Checkinternet()
    login.user_login_and_check_internet()

    driver = Check_Chrome_Driver()
    driver.check_driver_available()


def statuse_show():
    G = SingleTon_Variable()
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    G.app = app
    mainwindow = Pre_process()
    mainwindow.show()         
    app.exec()




def main():
    G = SingleTon_Variable()


    time.sleep(3)

    main_flow()
    # thread2 = threading.Thread(target = main_flow)  
    # thread2.start()
   
    
    print(G.user_password)
    print(G.chrome_driver_path)
    


main()

''' if __name__ == "__main__":
    main_flow() '''
