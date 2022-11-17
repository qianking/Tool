
#pre_process_controller

from login_ui_controller import Login

class Pre_process(QMainWindow):
    def __init__(self):
        super(Pre_process, self).__init__()
        
        self.set_windows()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(3)
        self.status_loading()
        self.start_proccess()

    def set_windows(self):
        """some widget set"""
    
    def status_loading(self):
        self.loading = Load_Thread()
        self.loading.signal.loading.connect(self.load_label)
        self.threadpool.start(self.loading)

    def start_proccess(self):
        self.get_proccess = Proccess_Thread()
        self.get_proccess.signal.login_window.connect(self.login_window)
        self.get_proccess.signal.status.connect(self.get_status_txt)

    def login_window(self, user_data):
        login = Login(user_data)
        login.show()  

    def get_status_txt(self, txt):
        self.loading.get_txt(txt)      

class thread_signal(QObject):
    login_window = Signal(str)
    status = Signal(str)
    loading = Signal(str)

class Proccess_Thread(QRunnable):
    def __init__(self):
        super(Proccess_Thread, self).__init__()  
        self.signal = thread_signal()
       
    def run(self):
        main(self.signal)


class Load_Thread(QRunnable):
    def __init__(self):
        super(Load_Thread, self).__init__() 
        self.signal = thread_signal()
        self.txt = 'Start'
        self.end_flag = False
        self.dot = ['.','..', '...']

    def run(self):
        while True :
            for i in self.dot:
                self.signal.loading.emit(f"{self.txt} {i}")
                time.sleep(1)
    
    def get_txt(self, txt):
        self.txt = txt


#login flow
def main(ui_signal):
    if not os.path.exists(user_data):
        ui_signal.login_window.emit(user_data) 
        #it will open login window in pre_process_controller 
        # I want it block process until login done
        user_data_list = read_and_get_userdata()
        return user_data_list


def read_and_get_userdata():
    """read user data file and return data in list"""


from login_ui import Ui_MainWindow  
"""import login_ui.py which is transfer from login_ui.ui made by Qt Designer"""

class Login(QMainWindow):
    def __init__(self, user_data, parent=None):
        QMainWindow.__init__(self, parent)
        self._window = Ui_MainWindow() 
        self._window.setupUi(self)
        """it will open a login window"""