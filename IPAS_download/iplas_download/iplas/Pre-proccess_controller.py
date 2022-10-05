import time
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal, Qt, QRunnable, QThreadPool, QObject
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QWidget, QGridLayout, QHBoxLayout
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
        self.start_proccess()
        self.start_loading()
    
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

        self.symbal = QLabel(self)
        self.symbal.setAlignment(Qt.AlignCenter)
        self.symbal.setFont(font)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label, 2)
        h_layout.addWidget(self.symbal, )

        g_layout = QGridLayout()    
        g_layout.addItem(h_layout, 0, 0, 0, 0)

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
    

    def start_loading(self):
        self.loading = Load_Thread()
        self.loading.signal.status.connect(self.load_label)
        self.threadpool.start(self.loading)
        self.load_label('...')

    def start_proccess(self):
        self.get_proccess = Proccess_Thread()
        self.get_proccess.signal.status.connect(self.done)
        self.threadpool.start(self.get_proccess)
        self.status_label(9)


    def load_label(self, text):
        self.symbal.setText(text) 
    
    def status_label(self, txt):
        self.label.setText(txt + ' '*2) 

    def done(self):
        self.close()  

class thread_signal(QObject):
    start = Signal(str)
    status = Signal(str)
    finish = Signal(str)
    
class Proccess_Thread(QRunnable):
    def __init__(self):
        super(Proccess_Thread, self).__init__()  
        self.signal = thread_signal()

    def run(self):
        IPLAS_Download.Get_Project_list(self.signal)


class Load_Thread(QRunnable):
    def __init__(self):
        super(Load_Thread, self).__init__() 
        self.signal = thread_signal()
        self.dot = ['.','..', '...']

    def run(self):
        while True :
            for i in self.dot:
                time.sleep(1)
                self.signal.status.emit(i) 


if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = Pre_process()
    mainwindow.show()         
    sys.exit(app.exec()) 