import sys
import re
from glob import glob
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtCore import QFile, QTimer, QDate, QTime, QThread, Signal, QObject, QPoint, QCoreApplication, Qt
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QFileDialog, QPlainTextEdit, QWidget, QDialog, QFontDialog, QTableWidget
from PySide6.QtGui import QColor, QPalette, QFont


class MainWindow(object):
    def __init__(self, parent=None):
        self._window = None
        self._widget = None
        self.folder_path = None
        self.setup_ui()
        

    @property
    def window(self):
        return self._window
    
    @property
    def widget(self):
        return self._widget

    def setup_ui(self):
        loader = QUiLoader()
        file = QFile('./pdf_UI_2.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()
        self.set_window_title()
        self.set_tab_tabwidget()
        self.set_in_tab_title()
        self.set_cover_label_text()
        self.set_config_btm()
        self.set_Audit_selection_radio_btm()
        self.line_edit_connect()
        self.txt_plain_connect()
        self.btm_connect()
        self.set_import_btm()
        self.set_start_btm()
        self.text_input_change()

        
        
#region 設定基本UI
    def set_window_title(self):
        self._window.setWindowTitle('PDF合併工具 V1.0.0')


    def set_tab_tabwidget(self):
        self.tabwidget = self._window.tabWidget
        self.tabwidget.setCurrentIndex(0)
        self.tab_title = ['核章版', '外審版']
        for i in range(len(self.tab_title)):
            self.tabwidget.setTabText(i, self.tab_title[i])

        text_font = QFont()
        text_font.setFamily('Times New Roman')
        text_font.setPointSize(12)
        
        style = """
        QTabBar::tab:selected {background: lightgray;}
        QTabWidget>QWidget>QWidget{background: lightgray; border: 2px solid black ;}       
        """
        self.tabwidget.setFont(text_font)
        self.tabwidget.setStyleSheet(style)
    
    def set_in_tab_title(self):
        self.tab_1_title_1 = self._window.tab_1_title_1
        self.tab_1_title_2 = self._window.tab_1_title_2
        tab_1 = [self.tab_1_title_1, self.tab_1_title_2]
        tab_1_txt = ['1. 所有欲合成的pdf檔名需包含目錄章節名稱，詳情請案右下角config按鈕查看', '2. 前兩大章節的檔案名稱請包含「資料結構」']
        for i in range(len(tab_1_txt)):
            tab_1[i].setText(tab_1_txt[i])

        self.tab_2_title_1 = self._window.tab_2_title_1
        self.tab_2_title_2 = self._window.tab_2_title_2
        tab_2 = [self.tab_2_title_1, self.tab_2_title_2]
        tab_2_txt = ['1. 所有欲合成的pdf檔名需包含目錄章節名稱，詳情請案右下角config按鈕查看', '1. 第一大章節的檔案名稱請包含「」']
        for i in range(len(tab_2_txt)):
            tab_2[i].setText(tab_2_txt[i])

        self.tab_3_title_1 = self._window.tab_3_title_1
        self.tab_3_title_2 = self._window.tab_3_title_2
        tab_3 = [self.tab_3_title_1, self.tab_3_title_2]
        tab_3_txt = []
        for i in range(len(tab_3_txt)):
            tab_3[i].setText(tab_3_txt[i])

        
        self.tab_1_title_3 = self._window.tab_1_title_3
        self.tab_2_title_3 = self._window.tab_2_title_3
        self.tab_3_title_3 = self._window.tab_3_title_3
        ps = [self.tab_1_title_3, self.tab_2_title_3, self.tab_3_title_3]
        ps_text = 'p.s. 本工具不會生成頁碼，請手動加入'
        for i in ps:
            i.setStyleSheet("color: #FF0000")
            i.setText(ps_text)
    

    def set_Audit_selection_radio_btm(self):
        self.audit_selection_1 = self._window.radioButton_1
        self.audit_selection_2 = self._window.radioButton_2
        self.audit_selection_3 = self._window.radioButton_3
        self.audit_selection_4 = self._window.radioButton_4
        self.audit_selection_group = self._window.buttonGroup

        self.selection_btm = [self.audit_selection_1, self.audit_selection_2, self.audit_selection_3, self.audit_selection_4]
        select_txt = ['第一次外審結構計算書', '第二次外審結構計算書', '第三次外審結構計算書', '會後意見回覆']
        for i in range(len(select_txt)):
            self.selection_btm[i].setFont(QFont('Times New Roman', 12, QFont.Bold))
            self.selection_btm[i].setText(select_txt[i])   


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
        self.config_3_btm = self._window.config_3_btm
        config_btm_list = [self.config_1_btm, self.config_2_btm, self.config_3_btm]
        for btm in config_btm_list:
            btm.setText('Config')
            
        #self.start_btm.setStyleSheet(button_style)
    
    def set_cover_label_text(self):
        self.groupbox = self._window.groupBox
        self.number_label = self._window.number
        self.address_label = self._window.address
        self.name_label = self._window.name
        self.file_name = self._window.file_name
        self.label = self._window.label
        self.label_V = self._window.label_V

        label_list = [self.number_label, self.label_V, self.address_label, self.name_label, self.file_name, self.label]
        label_txt = ['案號 : ',
                    'V',
                    '案名 : ',
                    '建築師 : ',
                    '檔名 : ',
                    '.pdf (選填，預設檔名為 Vooo_結構計算書(全))']
        for i in range(len(label_list)):
            label_list[i].setFont(QFont('Times New Roman', 12, QFont.Bold))
            label_list[i].setText(label_txt[i])
        self.groupbox.setFont(QFont('Times New Roman', 10))
        self.groupbox.setTitle('封面資訊')
#endregion


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
        self.folder_path = QFileDialog.getExistingDirectory(self._window, 'choose folder', 'F:/')
        self.folder_path = self.folder_path.replace("/", "\\")
        self.send_to_status(f"選擇資料夾: {self.folder_path}")
        

    def check_file(self):
        file_list = glob(f"{self.folder_path}\*.pdf")
        if len(file_list) == 0:
            self.send_to_status(f"未找到合法的pdf檔案，請重新選擇資料夾")
            self.folder_path = None
            self.start.setEnabled(False)
#endregion

#region start 按鈕動作
    def check_available(self):
        self.select_stytle = self.tabwidget.tabText(self.tabwidget.currentIndex())
        if self.select_stytle == '外審版':
            if self.audit_selection_group.checkedId() == -1:
                QMessageBox.warning(self._window, 'Warning', '請選擇外審版本', QMessageBox.Ok)
            else:
                radio_index = -(self.audit_selection_group.checkedId() + 2)
                self.Audit_selection = self.selection_btm[radio_index].text()
    
    def start_merge_thread(self):
        self.set_all_enable(False)
        self.start_merge = Merge_PDF_Thread(self.number, self.address, self.name, self.folder_path, self.file_name)
        self.start_merge.status.connect(self.send_to_status)
        self.start_merge.status.connect(self.set_enable)
        self.start_merge.start()
#endregion
    

    def send_to_status(self, txt):
        fft1 = self.status.currentCharFormat()
        if "WORNING" in txt or "ERROR" in txt:
            fft1.setForeground(Qt.red)
            
        else:  
            fft1.setForeground(Qt.black)
        self.status.setCurrentCharFormat(fft1)
        self.status.appendPlainText(txt)

    
    def get_information(self):
        self.number = self.number_input.text()
        self.address = self.address_input.text()
        self.name = self.name_input.text()
        
        if self.number != '' and self.address != '' and self.name != '' and self.folder_path != None:
            self.start.setEnabled(True)
        else:
            self.start.setEnabled(False)
        
        if self.file_name_input.text() == '':
            self.file_name = None
        else:
            self.file_name = self.file_name_input.text()

    
    def text_input_change(self):
        self.number_input.textChanged.connect(self.get_information)
        self.address_input.textChanged.connect(self.get_information)
        self.name_input.textChanged.connect(self.get_information)

        





if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.window.show()

    sys.exit(app.exec())

