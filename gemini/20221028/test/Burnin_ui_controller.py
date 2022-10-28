# -*- coding: UTF-8 -*-
import sys
import check_config

import time
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import QFile, QTimer, QRunnable, QThreadPool,Signal, Qt, QObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow
from PySide6.QtGui import QFont
from ui import Ui_MainWindow

config = {'config_error_msg': '', 
        'serial_name': 'Gemini', 
        'test_time': 8, 
        'terminal_server_comport': 'COM7', 
        'open_station': [0, 2003, 2004, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        'ftp_upload_path': '/SWITCH/EZ1K-ORT', 
        'online_function': True, 
        'op': 'LA2100645'}

config_path = r'.\config.ini'
                                         
VERSION = 'V0.00.24'

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self._window = Ui_MainWindow()
        self._window.setupUi(self)
        self.config_error_flag = False
        self.btm_flag = False
        self.running_process = ''
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.setup_ui()
        

    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        self.set_window_title()
        self.load_config()
        self.LCD_timer_set()
        self.set_online_lebal()
        self.start_btm()
        self.set_start_btm()
        self.define_checkbox_textpalin()
        self.init_all_checkbox()
        self.set_lebal_text()
        self.new_timer()
        
    
    def set_window_title(self):
        self.setWindowTitle(f'EZ1K_ORT {VERSION}')         

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
        config = check_config.check_config(config_path)

        print('config:', config)

        if config['config_error_msg']:
            self.config_error_flag = True
            self.custom_message('config error', config['config_error_msg'])
        
        config['VERSION'] = VERSION
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
    def get_start_time(self):
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
        self._window.label_time.setText(f"{str(config['test_time'])} h")
    
    def set_online_lebal(self):
        self.online = self._window.Online_line
        if config['online_function']:
            self.online.setText('ON')
        else:
            self.online.setText('OFF')

#region 開始按鍵要做的事
    #開始按鍵設定
    def start_btm(self):
        self.start = self._window.start_btm
        self.start.clicked.connect(self.start_burnin)  
    
    def set_start_btm(self):
        if self.config_error_flag:
            self.start.setEnabled(False)
        else:
            self.start.setEnabled(True)  
        
    #按開始後顯示請上電訊息
    def start_burnin(self):
        self.get_start_time()
        self.timer_start()
        self.start_burnin_thread()
        self.set_all_checkbox(('lightgreen', 'Ongoing..'))
        self.start.setEnabled(False)


    def start_burnin_thread(self):
        self.burnin_thread = Start_Burnin()
        self.burnin_thread.signal.single_light.connect(self.single_light_change)
        self.burnin_thread.signal.all_light.connect(self.set_all_checkbox)
        self.burnin_thread.signal.error_msg.connect(self.custom_message)
        self.burnin_thread.signal.finish.connect(self.test_finish)

        self.threadpool.start(self.burnin_thread)
#endregion

    def single_light_change(self, data:tuple):
        #num =
        #data = (telnet_port, statue)
        telnet_port, statue = data
        station_no = config['open_station'].index(telnet_port)
        if statue == 'fail':
            self.textplain_list[station_no].setStyleSheet("background : red")
            self.textplain_list[station_no].setText('\n      FAIL')
        if statue == 'done':
            self.textplain_list[station_no].setText('\n      Done')
    
    def test_finish(self):
        self.timer.stop()
        self.set_start_btm()
        
    

#region 1~20機的checkbox設定(顏色、字)
    def set_all_checkbox(self, data:tuple):
        color, txt = data
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


    #客製化messagebox
    @QtCore.Slot()
    def custom_message(self, data:dict):
        for title, msg in data.items():
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
    single_light = Signal(tuple)
    all_light = Signal(tuple)
    error_msg = Signal(dict)
    finish = Signal()

        
class Start_Burnin(QRunnable):
    def __init__(self):
        super(Start_Burnin, self).__init__()  
        self.signal = thread_signal()

    def run(self):
        Flow.Start_DUT_Initial(config = config,
                            signal = self.signal)     

if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.show()       

    sys.exit(app.exec())
   