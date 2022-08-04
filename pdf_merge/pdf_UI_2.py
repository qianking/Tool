import sys
import re
from glob import glob
import subprocess
import pdf_main
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtCore import QFile, QThread, Signal, Qt
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QPlainTextEdit
from PySide6.QtGui import QFont, QColor

VERSION = '1.0.0'

class MainWindow(object):
    def __init__(self, parent=None):
        self._window = None
        self.start_merge = None
        self.input_folder_path = None
        self.setup_ui()
        
    @property
    def window(self):
        return self._window

    def setup_ui(self):
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
        self.line_edit_connect()
        self.txt_plain_connect()
        self.btm_connect()
        self.set_import_btm()
        self.set_start_btm()
        self.text_input_change()

        
        
#region 設定基本UI
    def set_window_title(self):
        self._window.setWindowTitle(f'PDF合併工具 V {VERSION}')


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
        tab_1_txt = ['1. 所有欲合成的pdf檔名需包含目錄章節名稱，詳情請案右下角config按鈕查看', '2. 前兩大章節的檔案名稱請包含「資料結構」的字串']
        for i, tab in enumerate(tab_1):
            tab.setText(tab_1_txt[i])
        
        self.buid_single = self._window.single
        self.buid_muilti = self._window.muilti
        self.build_num_title = self._window.build_num
        self.build_No_title = self._window.build_No
        build_title = [self.buid_single, self.buid_muilti, self.build_num_title, self.build_No_title]
        build_title_txt = ['單棟', '多棟', '棟數 :', '編號 :']
        for i, build in enumerate(build_title):
            build.setFont(QFont('Times New Roman', 12))
            build.setText(build_title_txt[i])
        self.build_num_title.setAlignment(Qt.AlignRight)
        self.build_No_title.setAlignment(Qt.AlignRight)

        self.build_num_input = self._window.build_num_input
        self.build_No_input = self._window.build_No_input


    def set_Audit_tab(self):
        tab_title = '外審版'
        self.tabwidget.setTabText(1, tab_title)

        self.tab_2_title_1 = self._window.tab_2_title_1
        self.tab_2_title_2 = self._window.tab_2_title_2
        tab_2 = [self.tab_2_title_1, self.tab_2_title_2]
        tab_2_txt = ['1. 所有欲合成的pdf檔名需包含目錄章節名稱，詳情請案右下角config按鈕查看', '2. 第一大章節的檔案名稱請包含「外審意見回覆_n」(n為編號)']
        for i in range(len(tab_2_txt)):
            tab_2[i].setText(tab_2_txt[i])
        
        self.audit_selection_1 = self._window.radioButton_1
        self.audit_selection_2 = self._window.radioButton_2
        self.audit_selection_3 = self._window.radioButton_3
        self.audit_selection_4 = self._window.radioButton_4
        self.audit_selection_group = self._window.buttonGroup
        self.selection_btm = [self.audit_selection_1, self.audit_selection_2, self.audit_selection_3, self.audit_selection_4]
        self.select_txt = ['第一次外審結構計算書', '第二次外審結構計算書', '第三次外審結構計算書', '        會後意見回覆']
        for i, selection in enumerate(self.selection_btm):
            selection.setFont(QFont('Times New Roman', 12, QFont.Bold))
            selection.setText(self.select_txt[i].strip())   


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
        self.config_1_btm = self._window.config_1_btm
        self.config_2_btm = self._window.config_2_btm
        
        config_btm_list = [self.config_1_btm, self.config_2_btm]
        for btm in config_btm_list:
            btm.setText('Config')
        self.config_1_btm.clicked.connect(self.open_config_1_file)
        self.config_2_btm.clicked.connect(self.open_config_2_file) 
        #self.start_btm.setStyleSheet(button_style)
    
    def open_config_1_file(self):
        open_config_file(".\data\核章版檔名.txt")
    
    def open_config_2_file(self):
        open_config_file(".\data\外審版檔名.txt")

    
    def set_cover_label_text(self):
        self.groupbox = self._window.groupBox
        self.number_label = self._window.number
        self.address_label = self._window.address
        self.name_label = self._window.name
        self.file_name = self._window.file_name
        self.label = self._window.label
        self.label_V = self._window.label_V

        label_list = [self.number_label, self.address_label, self.name_label, self.file_name, self.label]
        label_txt = ['案號 : ',
                    '案名 : ',
                    '建築師 : ',
                    '檔名 : ',
                    '.pdf (選填，預設檔名為 Vooo_結構計算書(全))']
        for i, label in enumerate(label_list):
            label.setFont(QFont('Times New Roman', 12, QFont.Bold))
            label.setText(label_txt[i])
        self.label_V.setFont(QFont('Times New Roman', 12))
        self.label_V.setText('V')
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
        self.status.clear()
        self.input_folder_path = QFileDialog.getExistingDirectory(self._window, 'choose folder', 'F:/')
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
        if self.select_stytle == '外審版':
            if self.audit_selection_group.checkedId() == -1:
                QMessageBox.warning(self._window, 'Warning', '請選擇外審版本', QMessageBox.Ok)
            else:
                radio_index = -(self.audit_selection_group.checkedId() + 2)
                self.Audit_selection = self.select_txt[radio_index]
    
    def start_merge_thread(self):
        self.set_all_enable(False)
        data = self.select_stytle, self.number, self.address, self.name, self.input_folder_path, self.file_name
        if self.select_stytle == '核章版': 
            self.start_merge = Merge_PDF_Thread(data)
        if self.select_stytle == '外審版': 
            self.start_merge = Merge_PDF_Thread(data, Audit_selection=self.Audit_selection)
    
        self.start_merge.status.connect(self.send_to_status)
        self.start_merge.status.connect(self.set_enable)
        self.start_merge.start()
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
        if "WORNING" in txt or "ERROR" in txt:
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
        if "WORNING" in txt or "ERROR" in txt:
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
    def __init__(self, basic_data, **special_data):
        super(Merge_PDF_Thread, self).__init__()
        self.basic_data = basic_data
        self.special_data = special_data
    
    def run(self):
        self.special_data['self'] = self
        self.special_data['status'] = self.status
        pdf_main.main(self.basic_data,
                    self.special_data) 

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

