import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtCore import QFile, QThread, Signal, Qt, QRunnable, QThreadPool, QObject
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QMainWindow
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont, QColor, QIntValidator
from lfsdata_ui import Ui_MainWindow

VERSION = '0.01'

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
            file = QFile('./lfsdata_ui.ui')
            file.open(QFile.ReadOnly)
            self._window = loader.load(file)
            file.close()
        self.set_window_title()
        
        self.set_hint_label()

        self.set_import_btm()
        self.import_btm_connect()
        self.set_status_plain()
        self.set_table_title()
        self.set_table()
        self.set_table_default()
        self.set_num_label()
        self.set_floor_label()
        
        

    def set_window_title(self):
        if UI_file_format == 'ui':
            self._window.setWindowTitle(f'LFSD V {VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'LFSD V {VERSION}')            #.py版本
    
    def set_hint_label(self):
        self.hint_label_1 = self._window.label
        self.hint_label_2 = self._window.label_3

        self.hint_label_1.setFont(QFont('標楷體', 14, QFont.Bold))
        self.hint_label_1.setText('請輸入參數:')
        self.hint_label_2.setFont(QFont('標楷體', 14, QFont.Bold))
        self.hint_label_2.setText('請選擇資料夾')
        self.hint_label_2.setAlignment(Qt.AlignRight)
        
    
    def set_table_title(self):
        self.table_title_1 = self._window.label_1
        self.table_title_2 = self._window.label_2
        self.table_title_1.setFont(QFont('標楷體', 13))
        self.table_title_2.setFont(QFont('標楷體', 13))
        self.table_title_1.setText('混凝土磅數')
        self.table_title_1.setAlignment(Qt.AlignCenter)
        self.table_title_2.setText('各樓層樑深')
        self.table_title_2.setAlignment(Qt.AlignCenter)

    def set_table(self):
        self.table_1 = self._window.table_1
        self.table_2 = self._window.table_2
        table_title = [["樓層","fc'"], ["樓層","樑深"]]
        table_list = [self.table_1, self.table_2]

        for i, table in enumerate(table_list):
            self.table_setting(table, table_title[i])

    def table_setting(self, table, title):
        table.setColumnCount(2) #設置行數
        table.setRowCount(20)  #設置列數
        for i in range(20):
            for j in range(2):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table.setItem(i, j, item)
                table.openPersistentEditor(item)
        table.setHorizontalHeaderLabels([title[0], title[1]])
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
    
    def set_table_default(self):
        for i in range(20):
            item = QTableWidgetItem('F')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_2.setItem(i, 0, item)
    
    def set_num_label(self):
        self.num_label = self._window.num_label
        self.num_show = self._window.num_show
        self.num_show.setReadOnly(True)
        self.num_show.setFixedWidth(60)
        self.num_label.setText('案號 : ')
        self.num_label.setFont(QFont('標楷體', 13))
        self.num_label.setAlignment(Qt.AlignRight)
        self.num_show.setFont(QFont('Times New Roman', 13))

    def set_floor_label(self):
        self.floor_label = self._window.floor_label
        self.floor_show = self._window.floor_show
        self.floor_show.setReadOnly(True)
        self.floor_show.setFixedWidth(60)
        self.floor_label.setText('樓層 : ')
        self.floor_label.setFont(QFont('標楷體', 13))
        self.floor_label.setAlignment(Qt.AlignRight)
        self.floor_show.setFont(QFont('Times New Roman', 13))
    
    def set_num_floor_show(self, data):
        show_list = [self.num_show, self.floor_show]
        for ind, num in data.items():
            show_list[ind].setText(num)

    def set_import_btm(self):
        self.import_btm = self._window.import_btm
        self.import_btm.setText('Import')
        self.import_btm.setFont(QFont('Times New Roman', 12))
    
    def set_status_plain(self):
        self.status = self._window.status
        self.status.setReadOnly(True)
        self.status.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.status.setFont(QFont('Times New Roman', 13))
        self.reset_status_palin()

    def import_btm_connect(self):
        self.import_btm.clicked.connect(self.select_folder)
        self.import_btm.clicked.connect(self.get_data)

    def select_folder(self):
        self.status.clear()
        self.input_folder_path = QFileDialog.getExistingDirectory(self, 'choose folder', 'F:/Job')
        self.input_folder_path = self.input_folder_path.replace("/", "\\")
        print(self.input_folder_path)
        self.send_to_status(f"選擇資料夾: {self.input_folder_path}")

    def reset_status_palin(self):
        self.status.clear()
    
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
    
    def get_data(self):
        tmp_table_1 = self.get_table_data(self.table_1)
        table_1_data = {i[0] : i[1] for i in tmp_table_1}
        tmp_table_2 = self.get_table_data(self.table_2)
        table_2_data = {i[0][:-1] : i[1] for i in tmp_table_2}
        print(table_2_data)

    def get_table_data(self, table):
        all_data = list()
        for row in range(table.rowCount()):
            tmp_list = list()
            for col in range(table.columnCount()):
                if table.item(row, col).text() == '' or table.item(row, col).text() == 'F':
                    continue
                tmp_list.append(table.item(row, col).text())
            if tmp_list:
                all_data.append(tmp_list)

        return all_data

    def start_thread(self):
        self.start_thread = start_process()
        self.start_thread.signals.status.connect(self.send_to_status)
        self.start_thread.signals.data_send.connect(self.set_num_floor_show)
        self.threadpool.start(self.start_thread)





class thread_signal(QObject):
    status = Signal(str)
    data_send = Signal(dict)

class start_process(QRunnable):
    def __init__(self):
        super(start_process, self).__init__()  
        self.signals = thread_signal()
        
    def run(self):
        pass




if '__main__' == __name__:
    UI_file_format = 'ui'
    
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