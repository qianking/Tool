from distutils.command.config import config
from genericpath import isfile
import sys
from glob import glob
import subprocess
import pdf_main
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtCore import QFile, QThread, Signal, Qt
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QMainWindow
from PySide6.QtGui import QFont, QColor, QIntValidator
from pdf_ui import Ui_MainWindow

UI_file_format = 'py'
VERSION = '0.04'

config_path = r".\config.ini"

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        if UI_file_format == 'py':
            self._window = Ui_MainWindow()
            self._window.setupUi(self)
        elif UI_file_format == 'ui':
            self._window = None               
        self.start_merge = None
        self.input_folder_path = None
        self.start_flage = True
        self.pdf_information = {}
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
        self.set_tab_tabwidget()
        self.set_Audit_tab()
        self.set_Stamp_tab()
        self.set_ps_in_tab()
        self.set_cover_label_text()
        self.set_config_btm()
        self.set_page_num_radio()
        self.line_edit_connect()
        self.txt_plain_connect()
        self.btm_connect()
        self.set_import_btm()
        self.set_start_btm()
        self.text_input_change()

        
        
#region 設定基本UI
    def set_window_title(self):
        if UI_file_format == 'ui':
            self._window.setWindowTitle(f'PDF合併工具 V {VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'PDF合併工具 V {VERSION}')             #.py版本

    def set_tab_tabwidget(self):
        self.tabwidget = self._window.tabWidget
        self.tabwidget.setCurrentIndex(0)
        text_font = QFont()
        text_font.setFamily('Times New Roman')
        text_font.setPointSize(12)
        
        style = """
        QTabBar::tab:selected {background: lightgray;}
        QTabWidget>QWidget>QWidget{background: lightgray; border: 2px solid black ;}       
        """
        self.tabwidget.setFont(text_font)
        self.tabwidget.setStyleSheet(style)
    
    def set_Stamp_tab(self):
        tab_title = '核章版' 
        self.tabwidget.setTabText(0, tab_title)

        self.tab_1_title_1 = self._window.tab_1_title_1
        self.tab_1_title_2 = self._window.tab_1_title_2
        tab_1 = [self.tab_1_title_1, self.tab_1_title_2]
        tab_1_txt = ['1. 所有欲合成的pdf檔名需包含目錄章節名稱，詳情請案右下角config按鈕查看', '2. 前兩大章節的檔名最前面加編號(02_0X)，\n   或包含「地震風力」字串(例: A&地震風力、B&地震風力...)']
        for i, tab in enumerate(tab_1):
            tab.setFont(QFont('標楷體', 14))
            tab.setText(tab_1_txt[i])
        
        self.buid_single = self._window.single
        self.buid_muilti = self._window.muilti
        self.build_num_title = self._window.build_num
        self.build_No_title = self._window.build_No
        self.tab_1_label = self._window.label_2
        self.stamp_selection_group = self._window.stamp_selection_group
        build_title = [self.buid_single, self.buid_muilti, self.build_num_title, self.build_No_title, self.tab_1_label]
        build_title_txt = ['單棟', '多棟', '棟數 :', '編號 :', "(請用「,」號分開，例 : A,B,C...)"]
        for i, build in enumerate(build_title):
            build.setFont(QFont('Times New Roman', 12))
            build.setText(build_title_txt[i])
        self.buid_single.setChecked(True)
        self.buid_single.toggled.connect(self.build_onclick_set)
        self.buid_muilti.toggled.connect(self.build_onclick_set)
        self.build_num_title.setAlignment(Qt.AlignRight)
        self.build_No_title.setAlignment(Qt.AlignRight)

        self.build_num_input = self._window.build_num_input
        self.build_num_input.setValidator(QIntValidator())
        self.build_No_input = self._window.build_No_input
        self.muilti_set = [self.build_num_title, self.build_No_title, self.tab_1_label, self.build_num_input, self.build_No_input]
        for i, build in enumerate(self.muilti_set):
            build.setFont(QFont('Times New Roman', 12))
            build.setEnabled(False)
    
    def build_onclick_set(self):
        if self.buid_muilti.isChecked():
            for i, build in enumerate(self.muilti_set):
                build.setEnabled(True)
        else:
            for i, build in enumerate(self.muilti_set):
                build.setEnabled(False)

    def set_Audit_tab(self):
        tab_title = '外審版'
        self.tabwidget.setTabText(1, tab_title)

        self.tab_2_title_1 = self._window.tab_2_title_1
        self.tab_2_title_2 = self._window.tab_2_title_2
        tab_2 = [self.tab_2_title_1, self.tab_2_title_2]
        tab_2_txt = ['1. 所有欲合成的pdf檔名需包含目錄章節名稱，詳情請案右下角config按鈕查看', '2. 第一大章節的檔案名稱請包含「外審意見回覆_n」(n為編號)']
        for i, tab in enumerate(tab_2):
            tab.setFont(QFont('標楷體', 14))
            tab.setText(tab_2_txt[i])
        
        self.audit_selection_1 = self._window.radioButton_1
        self.audit_selection_2 = self._window.radioButton_2
        self.audit_selection_3 = self._window.radioButton_3
        self.audit_selection_group = self._window.audit_selection_group
        self.selection_btm = [self.audit_selection_1, self.audit_selection_2, self.audit_selection_3]
        self.select_txt = ['第二次外審結構計算書', '第三次外審結構計算書', '        會後意見回覆']
        for i, selection in enumerate(self.selection_btm):
            selection.setFont(QFont('Times New Roman', 12, QFont.Bold))
            selection.setText(self.select_txt[i].strip())
        self.audit_selection_1.setChecked(True)  


    def set_ps_in_tab(self):
        self.tab_1_title_3 = self._window.tab_1_title_3
        self.tab_2_title_3 = self._window.tab_2_title_3
        ps = [self.tab_1_title_3, self.tab_2_title_3]
        ps_text = 'p.s. 本工具不會生成頁碼，請手動加入'
        for p in ps:
            p.setStyleSheet("color: #FF0000")
            p.setText(ps_text)


    def set_config_btm(self):
        ''' button_style = """
        QPushButton {
            
            background-color: #00aaff;
 
        }
        QPushButton:pressed {
            background-color: #FFA823;
            color: #000000;
            
        }
        """ '''
        self.config_btm = self._window.config_btm
        self.config_btm.setText('Config')
        self.config_btm.setFont(QFont('Times New Roman', 12))
        self.config_btm.clicked.connect(self.open_config_file) 
    
    def open_config_file(self):
        open_config_file(config_path)
    
    def set_page_num_radio(self):
        self.page_num = self._window.pagenum
        self.page_num.setText('頁碼')
        self.page_num.setFont(QFont('標楷體', 13))
    
    def set_cover_label_text(self):
        self.groupbox = self._window.groupBox
        self.number_label = self._window.number
        self.address_label = self._window.address
        self.name_label = self._window.name
        self.file_name = self._window.file_name
        self.label = self._window.label
        

        label_list = [self.number_label, self.address_label, self.name_label, self.file_name, self.label]
        label_txt = ['案號 : ',
                    '案名 : ',
                    '建築師 : ',
                    '檔名 : ',
                    '.pdf (選填，預設檔名為 Vooo_結構計算書)']
        for i, label in enumerate(label_list):
            label.setFont(QFont('Times New Roman', 12, QFont.Bold))
            label.setText(label_txt[i])
        self.groupbox.setFont(QFont('Times New Roman', 10))
        self.groupbox.setTitle('封面資訊')
#endregion

    def line_edit_connect(self):
        self.number_input = self._window.number_line
        self.address_input = self._window.address_line
        self.name_input = self._window.name_line
        self.file_name_input = self._window.file_name_line
        input_list = [self.number_input, self.address_input, self.name_input, self.file_name_input]
        for i in input_list:
            i.setFont(QFont('Times New Roman', 12))
        self.number_input.setText('V')


    def txt_plain_connect(self):
        self.status = self._window.status_txt
        self.status.setReadOnly(True)
        self.status.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.status.setFont(QFont('Times New Roman', 12))
        self.reset_status()

    
    def btm_connect(self):
        self.import_folder = self._window.import_btm
        self.start = self._window.start_btm
        self.start.setEnabled(False)

    
    def set_import_btm(self):
        self.import_folder.clicked.connect(self.open_folder)
        self.import_folder.clicked.connect(self.check_file)
        self.import_folder.clicked.connect(self.get_information)


    def set_start_btm(self):
        self.start.clicked.connect(self.get_information)
        self.start.clicked.connect(self.check_available)
        self.start.clicked.connect(self.start_merge_thread)

#region import 按鈕動作
    def open_folder(self):
        """ radio_index = -(self.audit_selection_group.checkedId() + 2)
        print('radio_index', radio_index)
        print('self.select_txt[radio_index]', self.select_txt[radio_index]) """
        self.status.clear()
        self.input_folder_path = QFileDialog.getExistingDirectory(self, 'choose folder', 'F:/Job')
        self.input_folder_path = self.input_folder_path.replace("/", "\\")
        self.send_to_status(f"選擇資料夾: {self.input_folder_path}")
        
        
    def check_file(self):
        file_list = glob(f"{self.input_folder_path}\*.pdf")
        if len(file_list) == 0:
            self.send_to_status(f"WORNING! 未找到pdf檔案，請重新選擇資料夾")
            self.input_folder_path = None
            self.start.setEnabled(False)
        else:
            self.send_to_status(f"找到{len(file_list)}個pdf檔案")
#endregion

#region start 按鈕動作
    def check_available(self):
        self.select_stytle = self.tabwidget.tabText(self.tabwidget.currentIndex())
        if self.select_stytle == '核章版':
            if self.buid_single.isChecked():
                self.pdf_information['select_stytle'] = 'Stamp_single'
            elif self.buid_muilti.isChecked():
                self.build_num = self.build_num_input.text()
                self.build_No = self.build_No_input.text()
                if self.build_num == "" or self.build_No == "":
                    self.start_flage = False
                    QMessageBox.warning(self._window, 'warning', '請填入棟數和編號', QMessageBox.Ok)

                elif self.build_num != "" and self.build_No != "":
                    self.build_No = [no.strip() for no in self.build_No.split(',')]
                    if len(self.build_No) != int(self.build_num):
                        self.start_flage = False
                        QMessageBox.warning(self._window, 'warning', '填入棟數和編號數目不匹配', QMessageBox.Ok)
                    else:
                        self.pdf_information['select_stytle'] = 'Stamp_multi'
                        self.pdf_information['build_num'] = int(self.build_num)
                        self.pdf_information['build_no'] = self.build_No

        if self.select_stytle == '外審版':
            radio_index = -(self.audit_selection_group.checkedId() + 2)
            self.pdf_information['select_stytle'] = 'Audit'
            self.pdf_information['Audit_selection'] = self.select_txt[radio_index]
        
    
    def start_merge_thread(self):
        if self.start_flage:
            self.pdf_information['input_folder_path'] = self.input_folder_path
            self.pdf_information['page_num'] = self.page_num.isChecked()
            self.set_all_enable(False)
            outline_infor_name = ['number', 'address', 'name', 'file_name']
            outline_information = [self.number, self.address, self.name, self.file_name]
            outline_information = dict(zip(outline_infor_name, outline_information))
            self.start_merge = Merge_PDF_Thread(outline_information, self.pdf_information)
        
            self.start_merge.status.connect(self.send_to_status)
            self.start_merge.status.connect(self.set_enable)
            self.start_merge.start()
        else:
            self.start_flage = True
#endregion
    
    def reset_status(self):
        self.status.clear()

        txt = '>>>>>>>請先確認選擇合併版本再開始<<<<<<<<'
        fft1 = self.status.currentCharFormat()
        fft1.setForeground(QColor('#da8318'))
        fft1.setFontWeight(QFont.Bold)
        self.status.setCurrentCharFormat(fft1)
        self.status.appendPlainText(txt)
        

    def send_to_status(self, txt):
        fft1 = self.status.currentCharFormat()
        if "WORNING" in txt or "Error" in txt:
            fft1.setForeground(Qt.red)
            
        elif '合併完成' in txt: 
            fft1.setForeground(Qt.blue)
        else:
            fft1.setForeground(Qt.black)
        self.status.setCurrentCharFormat(fft1)
        self.status.appendPlainText(txt)
    
    def set_all_enable(self, bool):
        self.start.setEnabled(bool)
        self.import_folder.setEnabled(bool)
        self.number_input.setEnabled(bool)
        self.address_input.setEnabled(bool)
        self.name_input.setEnabled(bool)
        self.file_name_input.setEnabled(bool)
        for btm in self.selection_btm:
            btm.setEnabled(bool)

    def set_enable(self, txt):
        if "WORNING" in txt or "Error" in txt:
            self.set_all_enable(True)
            if self.start_merge != None:
                self.start_merge.stop()
                print(self.start_merge.isRunning())
                self.start_merge = None
                self.input_folder_path = None
                self.start.setEnabled(False)

        elif '合併完成' in txt:
            self.set_all_enable(True)
            self.start_merge = None
            self.input_folder_path = None
            self.start.setEnabled(False)


    def text_input_change(self):
        self.number_input.textChanged.connect(self.get_information)
        self.address_input.textChanged.connect(self.get_information)
        self.name_input.textChanged.connect(self.get_information)
    
    def get_information(self):
        self.number = self.number_input.text()
        self.address = self.address_input.text()
        self.name = self.name_input.text()
        
        if self.number != '' and self.address != '' and self.name != '' and self.input_folder_path != None:
            self.start.setEnabled(True)
        else:
            self.start.setEnabled(False)
        
        if self.file_name_input.text() == '':
            self.file_name = None
        else:
            self.file_name = self.file_name_input.text()
    

def open_config_file(path):                              
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(["START",path], startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)   
    

        
class Merge_PDF_Thread(QThread):
    status = Signal(str)
    def __init__(self, ouline_information, pdf_information):
        super(Merge_PDF_Thread, self).__init__()
        self.outline_information = ouline_information
        self.pdf_information = pdf_information
        self.config = config_path
    
    def run(self):
        self.pdf_information['self'] = self
        self.pdf_information['status'] = self.status
        pdf_main.main(self.outline_information,
                    self.pdf_information, self.config) 

    def stop(self):
        self.terminate()


if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow()
    if UI_file_format == 'ui':
        mainwindow.window.show()  #.ui版本
    else:
        mainwindow.show()          #.py版本

    sys.exit(app.exec())

