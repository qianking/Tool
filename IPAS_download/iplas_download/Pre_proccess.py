import sys
import os
import time
import threading
from datetime import datetime
from iplas.Global_Variable import SingleTon_Variable, get_exception_detail
from iplas.user_login.User_Login import Login_and_Checkinternet
from iplas.lib.chromedriver_helper import Check_Chrome_Driver
import iplas.lib.create_log as create_log

G = SingleTon_Variable()

current_path = os.path.dirname(os.path.abspath(__file__))
upper_folder_path = '\\'.join(current_path.split('\\')[:-1])     #到上一層資料夾

docs_folder = fr"{upper_folder_path}\docs"   #使用者帳密在上一層資料夾中的data資料夾中
os.makedirs(docs_folder, exist_ok=True)
  
pre_proccess_log = fr"{upper_folder_path}\logs"
os.makedirs(pre_proccess_log, exist_ok=True)
pre_proccess_log = create_log.create_logger(fr"{pre_proccess_log}\pre_proccess.txt", 'pre_proccess_log')

G.docs_folder = docs_folder
G.logger = pre_proccess_log



def main_flow(signal = None):
    G = SingleTon_Variable()
    G.Send_to_UI.signal = signal

    tsk = []  
    login = Login_and_Checkinternet()
    thread1 = threading.Thread(target = login.user_login_and_check_internet)  
    thread1.start()  
    tsk.append(thread1)

    driver = Check_Chrome_Driver()
    thread2 = threading.Thread(target = driver.check_driver_available)  
    thread2.start()  
    tsk.append(thread2)

    for tt in tsk:
        tt.join()
    
    print(G.user_password)
    print(G.chrome_driver_path)
    


main_flow()

''' if __name__ == "__main__":
    main_flow() '''
