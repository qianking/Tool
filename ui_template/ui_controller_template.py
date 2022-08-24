import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtCore import QFile, QThread, Signal, Qt, QRunnable, QThreadPool, QObject
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QMainWindow
from PySide6.QtGui import QFont, QColor, QIntValidator
#from ui import Ui_MainWindow


VERSION = '1.0.1'



class MainWindow(QMainWindow):
    def __init__(self, UI_file_format, parent=None):
        super(MainWindow, self).__init__()
        self.UI_file_format = UI_file_format
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
        if self.UI_file_format == 'ui':
            loader = QUiLoader()
            file = QFile('./ui.ui')
            file.open(QFile.ReadOnly)
            self._window = loader.load(file)
            file.close()
        self.set_window_title()
        if self.UI_file_format == 'ui':
            self._window.installEventFilter(self)


    #監看是否有關掉視窗的事件觸發 .ui版本
    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
        if (watched is self._window) and (event.type() == QtCore.QEvent.Close):
            reply = QMessageBox.question(self, 'Warning', 'sure?', QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()
                return True
        return super().eventFilter(watched, event)

    #監看是否有關掉視窗的事件觸發 .py版本
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', 'sure?', QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()
            return True
        return super().closeEvent(event)

    
    def set_window_title(self):
        if UI_file_format == 'ui':
            self._window.setWindowTitle(f'PDF合併工具 V {VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'PDF合併工具 V {VERSION}')             #.py版本


    

    def start_thread(self):
        self.start_init_thread = start_prcess()
        self.start_init_thread.signal.status.connect()
        self.threadpool.start(self.start_init_thread)




class thread_signal(QObject):
    status = Signal(dict)



class start_prcess(QRunnable):
    def __init__(self):
        super(start_prcess, self).__init__()  
        self.signal = thread_signal()
    
    def run(self):
        pass




if '__main__' == __name__:

    UI_file_format = 'py'
    
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow(UI_file_format)
    if UI_file_format == 'ui':
        mainwindow.window.show()  #.ui版本
    else:
        mainwindow.show()          #.py版本

    sys.exit(app.exec())