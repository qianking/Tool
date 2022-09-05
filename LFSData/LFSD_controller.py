import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtCore import QFile, QThread, Signal, Qt, QRunnable, QThreadPool, QObject
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QMainWindow
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont, QColor, QIntValidator
#from ui import Ui_MainWindow


VERSION = '0.01'


#討論表格填入的數據的流程



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
            file = QFile('./lfsd_ui.ui')
            file.open(QFile.ReadOnly)
            self._window = loader.load(file)
            file.close()
        self.set_window_title()
        self.FC_table()
        self.set_import_btm()
        self.set_table_default()
        self.insert_row_btm()

    
    def set_window_title(self):
        if UI_file_format == 'ui':
            self._window.setWindowTitle(f'LFSD V {VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'LFSD V {VERSION}')             #.py版本

    
    def FC_table(self):
        self.fc_table = self._window.FC_table
        self.fc_table.setColumnCount(2) #設置行數
        self.fc_table.setRowCount(6)  #設置列數
        self.fc_table.setHorizontalHeaderLabels(['Floor','Pressure'])
        
        font = QFont('Arial', 12, QFont.Bold)
        self.fc_table.horizontalHeader().setFont(font)
        rows = self.fc_table.rowCount()
        for row in range(rows):
            self.fc_table.horizontalHeader().resizeSection(row,300) #設置每列的寬度
        #self.fc_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fc_table.verticalHeader().setVisible(False)
        self.fc_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #設置行自動延伸
        self.fc_table.horizontalHeader().setDefaultSectionSize(18)
        self.fc_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.fc_table.verticalScrollBar().setVisible(False)
        #self.fc_table.horizontalScrollBar().setVisible(False)
        
    
    def set_import_btm(self):
        self.import_btm = self._window.import_btm
        self.import_btm.clicked.connect(self.test)
    
    def test(self):
        nb_row = 6
        nb_col = 2
        for row in range(nb_row):
            for col in range(nb_col):
                print(row, col, self.fc_table.item(row, col).text())
    
    def test_2(self):
        row = self.fc_table.rowCount()
        self.fc_table.insertRow(row)
        
        item = QTableWidgetItem(str('l'))
        self.fc_table.setItem(row, 0, item)

    def set_table_default(self):
        items = ['0','1','2','3','4','6']
        for i, data in enumerate(items):
            item = QTableWidgetItem(str(data))
            self.fc_table.setItem(i, 0, item)
    
    def insert_row_btm(self):
        self.insert_row = self._window.insert_row_2
        self.insert_row.clicked.connect(self.test_2)

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