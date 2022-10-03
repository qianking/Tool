import time
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QFile, QThread, Signal, Qt, QRunnable, QThreadPool, QObject
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QWidget, QGridLayout
from PySide6.QtGui import QFont
import IPLAS_Download


class Pre_process(QMainWindow):
    def __init__(self):
        super(Pre_process, self).__init__()
        self.init_UI()

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        #self.startproject()
        #self.startthread()
        
    def init_UI(self):
        self.set_windows()
        self.set_frameless()

    def set_windows(self):
        self._widget = QWidget()
        self._width = 300
        self._height = 100
        self.setFixedSize(self._width, self._height)
        
        self.label = QLabel(self)
        font = QFont("Arial", 14, QFont.Bold)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)

        g_layout = QGridLayout()    
        g_layout.addWidget(self.label)

        self._widget.setLayout(g_layout)
        self.setCentralWidget(self._widget)
    
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
    

    def startthread(self):
        self.work = loadingThread()
        self.work.start()
        self.work.trigger.connect(self.updatelabel)
        self.work.setTerminationEnabled(True)
        self.updatelabel('...')
    
    def startproject(self):
        self.get_thread = getproject_thread()
        self.get_thread.signal.status.connect(self.done)
        self.threadpool.start(self.get_thread)

    def updatelabel(self, text):
        self.label.setText('Catch User Project  ' + text) 

    def done(self):
        self.close()  

class thread_signal(QObject):
    status = Signal(str)
    error = Signal(str)
    
class getproject_thread(QRunnable):
    def __init__(self):
        super(getproject_thread, self).__init__()  
        self.signal = thread_signal()

    def run(self):
        IPLAS_Download.Get_Project_list(self.signal)

class loadingThread(QThread):
    trigger = Signal(str)
    def __init__(self):
        super().__init__()
        self.dot = ['.','..', '...']

    def run(self):
        while True :
            for i in self.dot:
                time.sleep(0.3)
                self.trigger.emit(i) 


if '__main__' == __name__:
    
  
    
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow =Pre_process()
    mainwindow.show()         
    sys.exit(app.exec()) 