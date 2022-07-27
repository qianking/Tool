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
        self.start_merge = None
        self.folder_path = None
        
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
        self.input_change()

    def label_connect(self):
        self.title = self._window.title
        self.title_1 = self._window.title_1
        self.title_2 = self._window.title_2
        self.ps = self._window.ps
        self.number_label = self._window.number
        self.address_label = self._window.address
        self.name_label = self._window.name
        self.file_name = self._window.file_name
        self.label = self._window.label
        self.groupbox = self._window.groupBox
        
    
    def set_label_txt(self):
        label_list = [self.title, self.title_1, self.title_2]
        label_list_2 = [self.number_label, self.address_label, self.name_label, self.file_name, self.label]
        label_txt = ['合併規則 : ',
            '   1.要合併的pdf檔案請放在同意資料夾，並遵循檔名開頭為"oo_oo(章節數_小節數)"命名，檔名裡需包含小節的名子', 
                    '   2.本工具會自動生成目錄，目錄格式請見 "/cover/template.docx"']
        for i in range(len(label_list)):
            label_list[i].setFont(QFont('Times New Roman', 12))
            label_list[i].setText(label_txt[i])

        self.ps.setFont(QFont('Times New Roman', 12))
        self.ps.setStyleSheet("color: #FF0000")
        self.ps.setText('p.s. 本工具不會生成頁碼，請手動加入')
        
        label_txt_2 = ['案號 : ',
                    '地址 : ',
                    '名子 : ',
                    '檔名 : ',
                    '.pdf (選填，預設檔名為 Vooo_結構計算書(全))']
                    
        for i in range(len(label_list_2)):
            label_list_2[i].setFont(QFont('Times New Roman', 12, QFont.Bold))
            label_list_2[i].setText(label_txt_2[i])
        
        self.groupbox.setFont(QFont('Times New Roman', 10))
        self.groupbox.setTitle('封面資訊')

    
    def line_edit_connect(self):
        self.number_input = self._window.number_line
        self.address_input = self._window.address_line
        self.name_input = self._window.name_line
        self.file_name_input = self._window.file_name_line
        
    def txt_plain_connect(self):
        self.status = self._window.status_txt
        self.status.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.status.setFont(QFont('Times New Roman', 12))


    def btm_connect(self):
        self.import_folder = self._window.impoer_btm
        self.start = self._window.start_btm
        self.start.setEnabled(False)
        
    
    def set_import_btm(self):
        self.import_folder.clicked.connect(self.open_folder)
        self.import_folder.clicked.connect(self.check_pdf_file)
        self.import_folder.clicked.connect(self.get_information)
    
    def set_all_enable(self, bool):
        self.start.setEnabled(bool)
        self.import_folder.setEnabled(bool)
        self.number_input.setEnabled(bool)
        self.address_input.setEnabled(bool)
        self.name_input.setEnabled(bool)
        self.file_name_input.setEnabled(bool)

    
    def set_enable(self, txt):
        if "WORNING" in txt or "ERROR" in txt:
            self.set_all_enable(True)
            if self.start_merge != None:
                self.start_merge.stop()
                print(self.start_merge.isRunning())
                self.start_merge = None
                self.folder_path = None
                self.start.setEnabled(False)

        elif '合併完成' in txt:
            self.set_all_enable(True)

    def send_to_status(self, txt):
        fft1 = self.status.currentCharFormat()
        if "WORNING" in txt or "ERROR" in txt:
            fft1.setForeground(Qt.red)
            
        else:  
            fft1.setForeground(Qt.black)
        self.status.setCurrentCharFormat(fft1)
        self.status.appendPlainText(txt)
    

    def open_folder(self):
        self.status.clear()
        self.folder_path = QFileDialog.getExistingDirectory(self._window, 'choose folder', 'F:/')
        self.folder_path = self.folder_path.replace("/", "\\")
        self.send_to_status(f"選擇資料夾: {self.folder_path}")

    
    def check_pdf_file(self):
        illegal_file_list = []
        patern = r'\d\d_\d\d'
        file_list = glob(f"{self.folder_path}\*.pdf")
        if len(file_list) != 0:
            self.send_to_status(f"找到 {len(file_list)} 個合法的pdf檔案")
            pdf_file_list = [i.split('\\')[-1] for i in file_list]
            for file in pdf_file_list:
                if_num = re.findall(patern, file)
                if len(if_num) == 0:
                    illegal_file_list.append(file)
            if len(illegal_file_list) != 0:
                file = '、'.join(illegal_file_list)
                self.send_to_status(f"WORNING! 有檔案未符合規定 : {file} \n已停止合併，請重新選擇資料夾")
                self.folder_path = None
                self.start.setEnabled(False)
        else:
            self.send_to_status(f"未找到合法的pdf檔案，請重新選擇資料夾")
            self.folder_path = None
            self.start.setEnabled(False)
        

    
    def get_information(self):
        self.number = self.number_input.text()
        self.address = self.address_input.text()
        self.name = self.name_input.text()
        if self.number != '' and self.address != '' and self.name != '' and self.folder_path != None:
            self.start.setEnabled(True)
        
        if self.file_name_input.text() == '':
            self.file_name = None
        else:
            self.file_name = self.file_name_input.text()


    def input_change(self):
        self.number_input.textChanged.connect(self.get_information)
        self.address_input.textChanged.connect(self.get_information)
        self.name_input.textChanged.connect(self.get_information)


    def start_merge_pdf(self):
        self.start.clicked.connect(self.get_information)
        self.start.clicked.connect(self.start_merge_thread)
    
    def start_merge_thread(self):
        self.set_all_enable(False)
        self.start_merge = Merge_PDF_Thread(self.number, self.address, self.name, self.folder_path, self.file_name)
        self.start_merge.status.connect(self.send_to_status)
        self.start_merge.status.connect(self.set_enable)
        self.start_merge.start()
            

    def select_font(self):   #查看字型用
        QFontDialog.getFont()


class Merge_PDF_Thread(QThread):
    status = Signal(str)
    def __init__(self, number, address, name, folder_path, file_name):
        super(Merge_PDF_Thread, self).__init__()
        self.number = number
        self.address = address
        self.name = name
        self.folder_path = folder_path
        self.file_name = file_name
    
    def run(self):
        pdf_main.main(self = self, 
                    status =  self.status,
                    number = self.number,
                    address = self.address,
                    name = self.name,
                    folder_path = self.folder_path,
                    final_file_name = self.file_name
                    )

    def stop(self):
        self.terminate()   




if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.window.show()

    sys.exit(app.exec())