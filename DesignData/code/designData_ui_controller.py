import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QFile, QThread, Signal, Qt, QRunnable, QThreadPool, QObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
import Main as transfer
from designdata_ui import Ui_MainWindow

UI_file_format = 'py'
VERSION = '0.03'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        if UI_file_format == 'py':
            self._window = Ui_MainWindow()
            self._window.setupUi(self)
        elif UI_file_format == 'ui':
            self._window = None  

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)     
        self.setup_ui()

    @property
    def window(self):
        return self._window

    def setup_ui(self):
        if UI_file_format == 'ui':
            loader = QUiLoader()
            file = QFile('./DesignData_ui.ui')
            file.open(QFile.ReadOnly)
            self._window = loader.load(file)
            file.close()
        self.set_window_title()
        self.Input_btm()
        self.filename_lineedit()
        self.plain_txt()
        
    
    def set_window_title(self):
        if UI_file_format == 'ui':
            self._window.setWindowTitle(f'DesignData V {VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'DesignData V {VERSION}')             #.py版本
    
    def Input_btm(self):
        self.Input = self._window.input_btm
        self.Input.clicked.connect(self.open_file)
        self.Input.clicked.connect(self.start_thread)

    def filename_lineedit(self):
        self.showfilename = self._window.lineEdit 
    
    def open_file(self):
        self.show_information.clear()
        self.input_path, filetype = QFileDialog.getOpenFileName(self, 'Open folder', 'F:/', "txt (*txt)")
        print(self.input_path)
        self.input_path = self.input_path.replace('/', '\\')
        self.showfilename.setText(self.input_path)

    def start_thread(self):
        self.start_thread = start_process(self.input_path)
        self.start_thread.signals.status.connect(self.send_to_status)
        self.threadpool.start(self.start_thread)
    
    def plain_txt(self):
        self.show_information = self._window.plainTextEdit

    def send_to_status(self, txt):
        fft1 = self.show_information.currentCharFormat()
        if "WORNING" in txt or "Error" in txt:
            fft1.setForeground(Qt.red)
            self.show_information.setCurrentCharFormat(fft1)
            self.show_information.insertPlainText(f"{txt}\n")
        
        elif '轉換完成' in txt: 
            fft1.setForeground(Qt.blue)
            self.show_information.setCurrentCharFormat(fft1)
            self.show_information.insertPlainText(f"{txt}\n")

        elif ': ' in txt:
            txt_list = txt.split(': ')
            fft1.setForeground(Qt.darkGreen)
            self.show_information.setCurrentCharFormat(fft1)
            self.show_information.insertPlainText(f"{txt_list[0]}: ")
            fft1.setForeground(Qt.black)
            self.show_information.setCurrentCharFormat(fft1)
            self.show_information.insertPlainText(f"{txt_list[1]}\n")


class thread_signal(QObject):
    status = Signal(str)

class start_process(QRunnable):
    def __init__(self, input_path):
        super(start_process, self).__init__()  
        self.signals = thread_signal()
        self.input_path = input_path
        
    def run(self):
        transfer.Transfer_Flow(self.input_path, self.signals)

    
if '__main__' == __name__:
    #QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow_1 = MainWindow()
    if UI_file_format == 'ui':
        mainwindow_1.window.show()  #.ui版本
    else:
        mainwindow_1.show()          #.py版本

    sys.exit(app.exec())

