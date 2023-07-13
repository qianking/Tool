import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QFile, QThread, Signal, Qt, QRunnable, QThreadPool, QObject, QRegularExpression
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QMainWindow, QLineEdit
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont, QColor, QIntValidator, QRegularExpressionValidator
from lfsdata_ui import Ui_MainWindow
from glob import glob

import LFS_Main_Flow

VERSION = '0.05'

class MainWindow(QMainWindow):
    def __init__(self, UI_file_format, parent=None):
        super(MainWindow, self).__init__()
        self.UI_file_format = UI_file_format
        self.data = dict()
        self.start_flag = False

        self.column_num = 3
        self.row_num = 20

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
            file = QFile('./lfsdata_ui.ui')
            file.open(QFile.ReadOnly)
            self._window = loader.load(file)
            file.close()
        self.set_window_title()
        self.set_hint_label()
        self.set_import_btm()
        self.set_start_btm()
        self.import_btm_connect()
        self.start_btm_connect()
        self.set_status_plain()
        self.set_table()
        self.set_num_label()
        self.set_floor_label()
         

    def set_window_title(self):
        if UI_file_format == 'ui':
            self._window.setWindowTitle(f'LFSD V{VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'LFSD V{VERSION}')            #.py版本
    
    def set_hint_label(self):     
        self.hint_label_2 = self._window.label_3
        self.hint_label_2.setFont(QFont('標楷體', 12, QFont.Bold))
        self.hint_label_2.setText('請先選擇資料夾')
        self.hint_label_2.setAlignment(Qt.AlignCenter)

    def set_table(self):
        self.table_1 = self._window.table_1       
        table_title = ["樓層", "fc'", "梁深(m)"]
        self.table_setting(self.table_1, table_title)

    def table_setting(self, table, title):
        table.setColumnCount(self.column_num) #設置行數
        table.setRowCount(self.row_num)  #設置列數
        for i in range(self.row_num):
            for j in range(self.column_num):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table.setItem(i, j, item)
                table.openPersistentEditor(item)
                #ceil = QLineEdit()
                #validator = QRegularExpressionValidator(QRegularExpression("\d+[.]?\d+"), ceil) #設置只能輸入數字
                #ceil.setValidator(validator)
                #table.setCellWidget(i, j, ceil)

        table.setHorizontalHeaderLabels([title[0], title[1], title[2]])
        font = QFont('標楷體', 12, QFont.Bold)
        table.horizontalHeader().setFont(font)
        rows = table.rowCount()
        for row in range(rows):
            table.horizontalHeader().resizeSection(row, 300) #設置每列的寬度
        #self.fc_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #設置行自動延伸
        table.horizontalHeader().setDefaultSectionSize(18)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        #self.fc_table.verticalScrollBar().setVisible(False)
        #self.fc_table.horizontalScrollBar().setVisible(False)
    
    def set_num_label(self):
        self.num_label = self._window.num_label
        self.num_show = self._window.num_result
        self.num_show.setText("----")
        self.num_show.setFixedWidth(60)
        self.num_label.setText('案號 : ')
        self.num_label.setFont(QFont('標楷體', 13))
        self.num_label.setAlignment(Qt.AlignRight)
        self.num_show.setFont(QFont('Times New Roman', 13))

    def set_floor_label(self):
        self.floor_label = self._window.floor_label
        self.floor_show = self._window.floor_result
        self.floor_show.setText("----")
        self.floor_show.setFixedWidth(60)
        self.floor_label.setText('樓層 : ')
        self.floor_label.setFont(QFont('標楷體', 13))
        self.floor_label.setAlignment(Qt.AlignRight)
        self.floor_show.setFont(QFont('Times New Roman', 13))
    
    def set_num_floor_result(self, data):
        self.num_show.setText(data.get('num'))    
        self.floor_show.setText(data.get('floor_num'))
        self.data['num'] = data.get('num')
        self.data['floor_num'] = data.get('floor_num')

    def set_import_btm(self):
        self.import_btm = self._window.import_btm
        self.import_btm.setText('Import')
        self.import_btm.setFont(QFont('Times New Roman', 12))

    def set_start_btm(self):
        self.start_btm = self._window.start_btm
        self.start_btm.setText('Start')
        self.start_btm.setFont(QFont('Times New Roman', 12))
    
    def set_status_plain(self):
        self.status = self._window.status
        self.status.setReadOnly(True)
        self.status.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.status.setFont(QFont('Times New Roman', 13))

    def select_folder(self):
        self.status.clear()
        input_folder_path = QFileDialog.getExistingDirectory(self, 'choose folder', 'F:/Job')
        input_folder_path = input_folder_path.replace("/", "\\")
        self.show_status((f"選擇路徑: {input_folder_path}", Qt.black))
        file_list = glob(f"{input_folder_path}\*.txt")

        self.data['input_path'] = input_folder_path
        self.data['file_list'] = file_list
        self.data['file_name_dic'] = {file.split('\\')[-1].split('.')[0]: file for file in file_list}
        for file in file_list:
            file = file.split('\\')[-1]
            self.show_status((f"   {file}", Qt.black))
        self.show_status((f"總共發現{len(file_list)}個檔案", Qt.darkYellow))
        

    def reset_all(self):
        self.set_table()
        self.status.clear()
        self.num_show.setText('')
        self.floor_show.setText('')

    def show_status(self, show_data:tuple):
        print(show_data)
        txt, color = show_data
        fft1 = self.status.currentCharFormat()
        fft1.setForeground(color)     
        self.status.setCurrentCharFormat(fft1)
        self.status.insertPlainText(f"{txt}\n")

    def set_table_floor_data(self, floor_data:list):
        self.row_num = len(floor_data)
        self.set_table()
        for i, data in enumerate(floor_data):
            self.table_1.setItem(i, 0, QTableWidgetItem(data))   
        self.data['floor_data'] = floor_data    

    def get_data_from_table(self):
        self.data['FC'] = self.get_table_data(self.table_1, 1)
        self.data['HNDL'] = self.get_table_data(self.table_1, 2)
        
    def get_table_data(self, table, column):
        all_data = dict()
        for row in range(table.rowCount()):
            if table.cellWidget(row, column).text() == '':
                continue
            all_data[table.cellWidget(row, 0).text()] = table.cellWidget(row, column).text()
        if len(all_data) == 0:
            self.show_status(("請檢查FC或是HNDL是否填入!", Qt.red))
        return all_data
    
    def import_btm_connect(self):
        self.import_btm.clicked.connect(self.select_folder)
        self.import_btm.clicked.connect(self.start_getfloordata_thread)
    
    def start_btm_connect(self):
        self.start_btm.clicked.connect(self.get_data_from_table)
        self.start_btm.clicked.connect(self.start_ouput_thread)
    
    def start_getfloordata_thread(self):
        self.start_get_thread = start_get_floor_data_proccess(self.data)
        self.start_get_thread.signals.status.connect(self.show_status)
        self.start_get_thread.signals.result_send.connect(self.set_num_floor_result)
        self.start_get_thread.signals.floor_data_send.connect(self.set_table_floor_data)
        self.start_get_thread.signals.reset_all.connect(self.reset_all)

        self.threadpool.start(self.start_get_thread)      

    def start_ouput_thread(self):
        print(self.data)
        self.start_thread = start_process(self.data)
        self.start_thread.signals.status.connect(self.show_status)
        self.start_thread.signals.reset_all.connect(self.reset_all)
        self.threadpool.start(self.start_thread)



class thread_signal(QObject):
    status = Signal(tuple)
    floor_data_send = Signal(list)
    result_send = Signal(dict)
    reset_all = Signal()

class start_get_floor_data_proccess(QRunnable):
    def __init__(self, input_path):
        super(start_get_floor_data_proccess , self).__init__()  
        self.signals = thread_signal()
        self.input_path = input_path

    def run(self):
        LFS_Main_Flow.Get_FloorData_Flow(self.input_path, self.signals)


class start_process(QRunnable):
    def __init__(self, data):
        super(start_process, self).__init__()  
        self.signals = thread_signal()
        self.data = data
        
    def run(self):
        LFS_Main_Flow.Main_Flow(self.data, self.signals)




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