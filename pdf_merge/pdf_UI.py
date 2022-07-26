import sys
import re
from glob import glob
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtCore import QFile, QTimer, QDate, QTime, QThread, Signal, QObject, QPoint, QCoreApplication, Qt
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QFileDialog, QPlainTextEdit, QWidget, QDialog, QFontDialog
from PySide6.QtGui import QColor, QPalette, QFont
import pdf_main


class MainWindow(object):
    def __init__(self, parent=None):
        self._window = None
        self.setup_ui()

    @property
    def window(self):
        return self._window

    def setup_ui(self):
        loader = QUiLoader()
        file = QFile('./pdf_UI.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()
        #self.check_font()
        self.label_connect()
        self.line_edit_connect()
        self.txt_plain_connect()
        self.btm_connect()
        self.set_label_txt()
        self.set_import_btm()
        self.start_merge_pdf()

    def label_connect(self):
        self.title_1 = self._window.title_1
        self.title_2 = self._window.title_2
        self.title_3 = self._window.title_3
        self.number_label = self._window.number
        self.address_label = self._window.address
        self.name_label = self._window.name
        self.groupbox = self._window.groupBox
        
    
    def set_label_txt(self):
        label_list = [self.title_1, self.title_2, self.title_3, self.number_label, self.address_label, self.name_label]
        label_txt = ['1.要合併的pdf檔案請遵循檔名開頭為"XX_XX(章節數_小節數)"命名，檔名裡需包含小節的名子', 
                    '2.本工具會自動生成目錄，目錄格式請見 "/cover/template.docx"',
                    '3.本工具不會生成頁碼，請手動加入',
                    '案號 : ',
                    '地址 : ',
                    '名子']
        for i in range(len(label_list)):
            label_list[i].setFont(QFont('Times New Roman', 12))
            label_list[i].setText(label_txt[i])
        
        self.groupbox.setTitle('封面資訊')

    
    def line_edit_connect(self):
        self.number_input = self._window.number_line
        self.address_input = self._window.address_line
        self.name_input = self._window.name_line
        
    def txt_plain_connect(self):
        self.status = self._window.status_txt
        self.status.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.status.setFont(QFont('Times New Roman', 12))


    def btm_connect(self):
        self.import_folder = self._window.impoer_btm
        self.start = self._window.start_btm
        
    
    def set_import_btm(self):
        self.import_folder.clicked.connect(self.open_folder)
        self.import_folder.clicked.connect(self.check_pdf_file)
    
    def send_to_status(self, txt):
        fft1 = self.status.currentCharFormat()
        if "WORNING" in txt or "ERROR" in txt:
            fft1.setForeground(Qt.red)
            self.status.setCurrentCharFormat(fft1)
        self.status.appendPlainText(txt)
    

    def open_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self._window, 'choose folder', 'C:/')
        self.folder_path = self.folder_path.replace("/", "\\")
        self.send_to_status(f"選擇資料夾: {self.folder_path}")

    
    def check_pdf_file(self):
        illegal_file_list = []
        patern = r'\d\d_\d\d'
        file_list = glob(f"{self.folder_path}\*.pdf")
        self.send_to_status(f"找到 {len(file_list)} 個pdf檔案")
        pdf_file_list = [i.split('\\')[-1] for i in file_list]
        for file in pdf_file_list:
            if_num = re.findall(patern, file)
            if len(if_num) == 0:
                illegal_file_list.append(file)
        if len(illegal_file_list) != 0:
            file = '、'.join(illegal_file_list)
            self.send_to_status(f"WORNING! 有檔案未符合規定 : {file}")

    
    def get_information(self):
        self.number = self.number_input.text()
        self.address = self.address_input.text()
        self.name = self.name_input.text()
        

    def start_merge_pdf(self):
        self.start.clicked.connect(self.get_information)
        self.start.clicked.connect(self.start_merge_thread)
    
    def start_merge_thread(self):
        self.start_merge = Merge_PDF_Thread(self.number, self.address, self.name, self.folder_path)
        self.start_merge.status.connect(self.send_to_status)
        self.start_merge.start()
            

    def select_font(self):   #查看字型用
        QFontDialog.getFont()


class Merge_PDF_Thread(QThread):
    status = Signal(str)
    def __init__(self, number, address, name, folder_path):
        QThread.__init__(self)
        self.number = number
        self.address = address
        self.name = name
        self.folder_path = folder_path
    
    def run(self):
        pdf_main.main(self = self, 
                    status =  self.status,
                    number = self.number,
                    address = self.address,
                    name = self.name,
                    folder_path = self.folder_path
                    )

        




if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.window.show()

    sys.exit(app.exec())