# -*- coding: UTF-8 -*-
import sys
import check_config
import ORT_Test_Flow as Flow
import time
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import QFile, QTimer, QRunnable, QThreadPool,Signal, Qt, QObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow
from PySide6.QtGui import QFont
from ui import Ui_MainWindow

config = {'config_error_msg': '', 
        'serial_name': 'EZ1K_A1', 
        'serial_port': 8, 
        'test_time': 24, 
        'package_machine': 'Nustream', 
        'terminal_server_comport': 'COM4', 
        'pg_comport': 'COM5', 
        'open_station': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        'ftp_upload_funtion': True, 
        'ftp_upload_path': '/SWITCH/EZ1K-ORT',
        'SFIS_function': True,
        'op':'LA2100645'}
                                         
dut_data = {2002: 'PSZ23261BCu'}

VERSION = 'V0.00.24'

class MainWindow(QMainWindow):
    def __init__(self, UI_file_format, parent=None):
        super(MainWindow, self).__init__()
        self.UI_file_format = UI_file_format
        if self.UI_file_format == 'py':
            self._window = Ui_MainWindow()
            self._window.setupUi(self)
        elif self.UI_file_format == 'ui':
            self._window = None
        self.config_error_flag = False
        self.package_btm_flag = False
        self.running_process = ''
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.setup_ui()
        

    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        if self.UI_file_format == 'ui':
            loader = QUiLoader()
            file = QFile('./ui.ui')
            file.open(QFile.ReadOnly)
            self._window = loader.load(file)
            file.close()
        self.set_window_title()
        self.load_config()
        self.LCD_timer_set()
        self.set_ftp_sfis_lebal()
        self.start_btm()
        self.set_start_btm()
        self.loop_btm()
        self.set_loop_btm()
        self.define_checkbox_textpalin()
        self.init_all_checkbox()
        self.set_lebal_text()
        self.new_timer()
        
        if self.UI_file_format == 'ui':
            self._window.installEventFilter(self)
     

    def set_window_title(self):
        if self.UI_file_format == 'ui':
            self._window.setWindowTitle(f'EZ1K_ORT {VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'EZ1K_ORT {VERSION}')             #.py版本

    #監看是否有關掉視窗的事件觸發
    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
        if (watched is self._window) and (event.type() == QtCore.QEvent.Close):
            reply = QMessageBox.question(self, 'Warning', 'sure?', QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()
                return True
        return super().eventFilter(watched, event)

    #監看是否有關掉視窗的事件觸發.py版本
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', 'sure?', QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()
            return True
        return super().closeEvent(event)
    

#region 載入config.ini內的資料
    def load_config(self):
        global config
        config = check_config.check_config('./config.ini')

        print('config:', config)

        if config['config_error_msg']:
            self.config_error_flag = True
            self.custom_message('config error', config['config_error_msg'])
#endregion
    

#region 計時器設定
    #設定計時器格式
    def LCD_timer_set(self):
        self.lcd = self._window.lcdNumber
        self.lcd.setDigitCount(11)
        self.lcd.setStyleSheet("border: 2px solid black; color: black;")
        self.initial = '00' + ":" + '00' + ":" + '00' + ":" + '00'
        self.lcd.display(self.initial)

    #設定開始時間
    def start_time(self):
        self.startTime = time.time()
        #self.startTime = QDateTime.currentSecsSinceEpoch()
    
    def new_timer(self):
        self.timer = QTimer(self)

    #計時器開始
    def timer_start(self):
        self.timer.timeout.connect(self.timer_refresh)
        self.timer.start(1000) 
   
    #計時器更新(每秒)
    def timer_refresh(self):
        self.now = time.time()
        self.interval = round(self.now - self.startTime)
        
        if self.interval > 0:
            days = self.interval // (24 * 60 * 60)
            hours = (self.interval - days *(24 * 60 * 60)) // (60 * 60)
            mins = (self.interval - days *(24 * 60 * 60 ) - hours *(60 * 60 )) //(60)
            secs = (self.interval - days *(24 * 60 * 60 ) - hours *(60 * 60 ) - mins *(60))
            if days // 10 == 0:
                days = '0' + str(days)

            if hours // 10 == 0:
                hours = '0' + str(hours)

            if mins // 10 == 0:
                mins = '0' + str(mins)

            if secs // 10 == 0:
                secs = '0' + str(secs)
            
            self.intervals = str(days) + ":" + str(hours) + ":" + str(mins) + ":" + str(secs)
            self.lcd.display(self.intervals)
#endregion
   
    
#region 設定check box
    def init_all_checkbox(self):
        self.set_all_checkbox('lightgreen', 'Standby')

    def define_checkbox_textpalin(self):
        self.checkbox_list = [self._window.checkBox_1, self._window.checkBox_2, self._window.checkBox_3, self._window.checkBox_4, self._window.checkBox_5,
                              self._window.checkBox_6, self._window.checkBox_7, self._window.checkBox_8, self._window.checkBox_9, self._window.checkBox_10,
                              self._window.checkBox_11, self._window.checkBox_12, self._window.checkBox_13, self._window.checkBox_14, self._window.checkBox_15,
                              self._window.checkBox_16, self._window.checkBox_17, self._window.checkBox_18, self._window.checkBox_19, self._window.checkBox_20]
        self.textplain_list = [self._window.status_1, self._window.status_2, self._window.status_3, self._window.status_4, self._window.status_5,
                               self._window.status_6, self._window.status_7, self._window.status_8, self._window.status_9, self._window.status_10,
                               self._window.status_11, self._window.status_12, self._window.status_13, self._window.status_14, self._window.status_15,
                               self._window.status_16, self._window.status_17, self._window.status_18, self._window.status_19, self._window.status_20]   
#endregion

    
    #設定lebal文字
    def set_lebal_text(self):
        self._window.label_serial.setText(config['serial_name'])
        self._window.label_port.setText(str(config['serial_port']))
        self._window.label_package.setText(config['package_machine'])
        self._window.label_time.setText(f"{str(config['test_time'])} h")
    
    def set_ftp_sfis_lebal(self):
        self.ftp_line = self._window.FTP_line
        self.sfis_line = self._window.SFIS_line
        if config['ftp_upload_funtion']:
            self.ftp_line.setText('ON')
        else:
            self.ftp_line.setText('OFF')
            
        if config['SFIS_function']:
            self.sfis_line.setText('ON')
        else:
            self.sfis_line.setText('OFF')    

    def set_start_btm(self):
        if self.config_error_flag or self.package_btm_flag:
            self.start.setEnabled(False)
        else:
            self.start.setEnabled(True)    

    def set_loop_btm(self):
        if not self.package_btm_flag:
            self.loop.setEnabled(False)
        else: 
            self.loop.setEnabled(True) 
    

#region 開始按鍵要做的事
    #開始按鍵設定
    def start_btm(self):
        self.start = self._window.init_btm
        self.start.clicked.connect(self.start_clear_port)  
        
    #按開始後顯示請上電訊息
    def start_initial(self):
        self.start_time()
        self.timer_start()
        self.start_initial_thread()
        self.set_all_checkbox('lightgreen', 'Ongoing..')
        self.start.setEnabled(False)
        self.loop.setEnabled(False)
    
    def start_clear_port(self):
        self.start.setEnabled(False)
        self.start_clear_port_thread()

    def start_clear_port_thread(self):
        self.star_clear_port = start_Clear_Port_prcess()
        self.star_clear_port.signal.status.connect(self.event_process)
        self.threadpool.start(self.star_clear_port)
        
    def start_initial_thread(self):
        self.start_init_thread = start_initial_prcess()
        self.start_init_thread.signal.status.connect(self.event_process)
        self.threadpool.start(self.start_init_thread)
#endregion

    
#region 打封包按鍵要做的事
    def loop_btm(self):
        self.loop = self._window.loop_btm
        self.loop.clicked.connect(self.open_chamber_msg)
    
    def open_chamber_msg(self):
        reply = self.custom_message('information', '请打开chamber!')
        if reply == QMessageBox.Ok:    
            self.start_time()
            self.timer_start()
            self.start_packaging_thread()
            self.set_all_checkbox('lightgreen', 'Packaging..')
            self.start.setEnabled(False)
            self.loop.setEnabled(False)
    
    def start_packaging_thread(self):
        self.start_pack_thread = start_packaging_prcess()
        self.start_pack_thread.signal.status.connect(self.event_process)
        self.threadpool.start(self.start_pack_thread)
#endregion


#region 1~20機的checkbox設定(顏色、字)
    def set_all_checkbox(self, color, txt):
        for i in range(len(config['open_station'])): 
            if config['open_station'][i]:
                self.checkbox_list[i].setChecked(True) 
                self.textplain_list[i].setStyleSheet(f"background : {color}")
                
                font = QFont("Arial", 18, QFont.Black)
                self.textplain_list[i].setFont(font)
                self.textplain_list[i].setPlainText(txt)
                self.textplain_list[i].setAlignment(Qt.AlignCenter)
                #print(self.textplain_list[i].tabStopDistance())

                
            self.textplain_list[i].setReadOnly(True)
            self.checkbox_list[i].setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
            self.checkbox_list[i].setEnabled(False)
#endregion


#region 事件集中地
    def event_process(self, UI_msg):
        """
        用來處理module回傳的事件，用來改變UI介面的元件
        主要有:
        1. 單一狀態框改變
        2. 所有狀態框改變，如果改變為全fail，timer停止，所有thread都要停止，所有按鈕回到初始狀態
        3.message box跳出，當有message box，timer停止，所有thread都要停止，所有按鈕回到初始狀態
        4.terminal server清port，清完port才開始DUT測試
        5.初始化結束，改變按鈕flag讓打封包的按鈕可以按
        6.打封包結束，所有狀態回到初始狀態
        """
        global dut_data
        #print('UI_msg:', UI_msg)
        if 'single_status_change' in UI_msg:
            self.change_status_color(UI_msg['single_status_change'])
        
        if 'all_status_change' in UI_msg:
            self.set_all_checkbox(UI_msg['all_status_change'][0], UI_msg['all_status_change'][1])
            if UI_msg['all_status_change'][1] == 'Fail':
                self.event_stop_event()

        if 'messagebox_2' in UI_msg:
            reply = self.custom_message(UI_msg['messagebox_2'][0], UI_msg['messagebox_2'][1])
        
        if 'messagebox' in UI_msg:
            self.event_stop_event()
            reply = self.custom_message(UI_msg['messagebox'][0], UI_msg['messagebox'][1])    #挑出警示視窗，停止跑flow程式，並且回復到原始狀態，按鈕reset, 狀態燈回到standby
            if reply == QMessageBox.Ok:
                self.init_all_checkbox()
        
        if 'clear_port_end' in UI_msg:
            reply = self.custom_message('information', '请检查U盘连接并接上电源!')
            if reply == QMessageBox.Ok:
                self.start_initial()
        
        if 'initial_end' in UI_msg:
            self.package_btm_flag = True
            self.timer.stop()
            self.set_start_btm()
            self.set_loop_btm()  
            self.set_all_checkbox('lightgreen', 'PASS')
            self.custom_message('infomation', '初始设定完成!')
            dut_data = UI_msg['initial_end']
            
        if 'package_test_end' in UI_msg:
            self.package_btm_flag = False
            self.event_stop_event()
            self.set_all_checkbox('lightgreen', 'PASS')
            dut_data.clear()  #controller變數清空
        
    def event_stop_event(self):
        self.timer.stop()
        self.package_btm_flag = False
        dut_data.clear()
        
        self.set_start_btm()
        self.set_loop_btm()                 
#endregion   
         

    def change_status_color(self, data):
        #data=[機台, 字(狀態)]
        txt = data[1]
        station_no = data[0]
        
        if txt == 'FAIL':
            self.textplain_list[station_no].setStyleSheet("background : red")
            self.textplain_list[station_no].setText('\n      FAIL')
        
        if txt == 'PASS':
            self.textplain_list[station_no].setText('\n      PASS')  


    #客製化messagebox
    @QtCore.Slot()
    def custom_message(self, title, msg):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        font = QFont("Calibri", 15, QFont.Normal)
        msg_box.setFont(font)
        msg_box.show()
        
        retval = msg_box.exec()
        return retval



class thread_signal(QObject):
    status = Signal(dict)

class start_Clear_Port_prcess(QRunnable):
    def __init__(self):
        super(start_Clear_Port_prcess, self).__init__()  
        self.signal = thread_signal()
    
    def run(self):
        Flow.Start_Clear_Port(VERSION = VERSION, 
                            config = config,
                            signal = self.signal)
        
class start_initial_prcess(QRunnable):
    def __init__(self):
        super(start_initial_prcess, self).__init__()  
        self.signal = thread_signal()

    def run(self):
        
        Flow.Start_DUT_Initial(VERSION = VERSION,
                            config = config,
                            signal = self.signal)     

   
class start_packaging_prcess(QRunnable):
    def __init__(self):
        super(start_packaging_prcess, self).__init__() 
        self.signal = thread_signal() 
    
    def run(self):
        Flow.Packaging_Loop(VERSION = VERSION,
                            config = config,
                            signal = self.signal,
                            dut_data = dut_data,)
                

if '__main__' == __name__:
    UI_file_format = 'py'
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    #qt_app.setQuitOnLastWindowClosed(False)

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow(UI_file_format)
    if UI_file_format == 'ui':
        mainwindow.window.show()  #.ui版本
    else:
        mainwindow.show()          #.py版本

    sys.exit(app.exec())
   