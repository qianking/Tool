import time
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal, Qt, QRunnable, QThreadPool, QObject
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QWidget, QGridLayout, QHBoxLayout, QFileDialog
from PySide6.QtGui import QFont
import IPLAS_Download
#from Pre_proccess_UI import Ui_MainWindow

"""
檢查網路、檢查chrome driver版本，檢查是否有User Project
"""


class Pre_process(QMainWindow):
    def __init__(self):
        super(Pre_process, self).__init__()
        #self._window = Ui_MainWindow()
        #self._window.setupUi(self)
        
        self.init_UI()

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(2)
        self.choose_chrome_path()
        #self.start_proccess()
        #self.status_loading()
    
    ''' @property
    def window(self):
        return self._window '''
        
    def init_UI(self):
        self.set_windows()
        #self.set_label()
        self.set_frameless()

    def set_windows(self):
        self._widget = QWidget()
        self._width = 250
        self._height = 100
        #self.setGeometry(500, 500, self._width, self._height)
        self.setFixedSize(self._width, self._height)
        
        font = QFont("Arial", 14, QFont.Bold)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)

        g_layout = QGridLayout()    
        g_layout.addItem(self.label, 0, 0, 0, 0)

        self._widget.setLayout(g_layout)
        self.setCentralWidget(self._widget)
    
    ''' def set_label(self):
        self.label = self._window.label
        self.symbal = self._window.label_2
        font = QFont("Arial", 14, QFont.Bold)
        self.label.setFont(font)
        self.symbal.setFont(font) '''
    
    def set_frameless(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
    
    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched is self:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.mousePressEvent(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                self.mouseMoveEvent(event) 
        return super().eventFilter(watched, event)
    
    def mousePressEvent(self, event):
        self._old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta_x = int(event.globalPos().x()) - self._old_pos.x()
        delta_y = int(event.globalPos().y()) - self._old_pos.y()
        self.move(self.x() + delta_x, self.y() + delta_y)
        self._old_pos = event.globalPos()
    
    def error_box(self, txt):
        error_txt = f"預期外的錯誤!\n{txt}\n請聯絡開發者"
        ret = QMessageBox.critical(self, 'unexpected error', error_txt, QMessageBox.Ok)
        if ret == QMessageBox.Ok:
            self.close_window()
    
    def start_proccess(self):
        self.get_proccess = Proccess_Thread()
        self.get_proccess.signal.status.connect(self.status_loading)
        self.get_proccess.signal.error.connect(self.error_box)
        self.get_proccess.signal.finish.connect(self.close_window)
        self.threadpool.start(self.get_proccess)
    
    def status_loading(self, txt_tuple):

        self.loading = Load_Thread(txt_tuple)
        self.loading.signal.loading.connect(self.load_label)
        self.threadpool.start(self.loading)

    def load_label(self, text):
        self.label.setText(text)

    

    def close_window(self):
        self.close()  

class thread_signal(QObject):
    
    status = Signal(str)
    error = Signal(str)
    loading = Signal(str)
    finish = Signal()
    
class Proccess_Thread(QRunnable):
    def __init__(self):
        super(Proccess_Thread, self).__init__()  
        self.signal = thread_signal()

    def run(self):
        IPLAS_Download.Get_Project_list(self.signal)


class Load_Thread(QRunnable):
    def __init__(self, txt):
        super(Load_Thread, self).__init__() 
        self.signal = thread_signal()
        self.txt = txt
        self.end_flag = False
        self.dot = ['.','..', '...']

    def run(self):
        while True :
            for i in self.dot:
                if self.end_flag:
                    break
                self.signal.loading.emit(f"{self.txt} {i}")
                time.sleep(1)

    def end(self):
        self.end_flag = True


if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = Pre_process()
    mainwindow.show()         
    sys.exit(app.exec()) 