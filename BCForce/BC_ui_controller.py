import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QFile, QThread, Signal, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
import BC_transfer as transfer
from BC_ui import Ui_MainWindow

UI_file_format = 'py'
VERSION = '1.03'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        if UI_file_format == 'py':
            self._window = Ui_MainWindow()
            self._window.setupUi(self)
        elif UI_file_format == 'ui':
            self._window = None       
        self.setup_ui()

    @property
    def window(self):
        return self._window

    def setup_ui(self):
        if UI_file_format == 'ui':
            loader = QUiLoader()
            file = QFile('./pdf_UI_2.ui')
            file.open(QFile.ReadOnly)
            self._window = loader.load(file)
            file.close()
        self.set_window_title()
        self.Input_btm()
        self.filename_lineedit()
        self.plain_txt()
        
    
    def set_window_title(self):
        if UI_file_format == 'ui':
            self._window.setWindowTitle(f'BCForce V{VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'BCForce V{VERSION}')             #.py版本
    
    def Input_btm(self):
        self.Input = self._window.input_btm
        self.Input.clicked.connect(self.open_file)

    def filename_lineedit(self):
        self.showfilename = self._window.lineEdit
    
    def show_filename(self):
        self.showfilename.setText(self.File_path)
    
    def open_file(self):
        self.show_information.clear()
        self.File_path, filetype = QFileDialog.getOpenFileName(self, 'Open folder', 'F:/', "txt (*txt)")
        print(self.File_path)
        self.File_path = self.File_path.replace('/', '\\')
        self.show_filename()
        self.transfer_thread()
    
    def transfer_thread(self):
        self.transfer = Numerical_extraction_thread(self.File_path)
        self.transfer.status.connect(self.show_status)
        self.transfer.start()
    
    def plain_txt(self):
        self.show_information = self._window.plainTextEdit
    
    def show_status(self, txt):
        fft1 = self.show_information.currentCharFormat()
        if "WORNING" in txt or "Error" in txt or "警告" in txt:
            fft1.setForeground(Qt.red)
        else:
            fft1.setForeground(Qt.black)

        self.show_information.setCurrentCharFormat(fft1)
        self.show_information.insertPlainText(f"{txt}\n")


class Numerical_extraction_thread(QThread):
    status = Signal(str)
    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        transfer.main(input_path = self.path, self = self, status = self.status)

    
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

