from ast import Global
import sys
sys.path.append(r".\my lib")
import Download_isn
import write_set_schedular
from User_login import return_user_data
import chromedriver_helper
import file_util
import os
import datetime
import time
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile, QTimer, QDate,QTime, QThread,Signal, QObject, QPoint
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QColor, QBrush, QTextCharFormat ,QCursor, QTextCursor, QTextBlockFormat ,QTextFrameFormat,QMouseEvent
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QFileDialog, QPlainTextEdit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from requests_ntlm import HttpNtlmAuth
import glob

chromedriver_helper.check_driver_available()
password = return_user_data()
#13456

IPLAS_log_path = r"C:\littleTooldata\IPLAS\logs"
IPLAS_data_path = r"C:\littleTooldata\IPLAS\data"
download_path = r'C:\littleTooldata\IPLAS\Download'
schedule_data_path = r"C:\littleTooldata\IPLAS\Schedule_data\data"
#IPLAS_userproject_path = f"{IPLAS_data_path}\userprojcet.txt"
IPLAS_defaultset_path = f"{IPLAS_data_path}\default.json"

IPLAS_url = "http://cnsiplas.sz.pegatroncorp.com/iPLAS"
IPLAS_UI_logger = file_util.create_logger(IPLAS_log_path, 'IPLAS_log')

project = ['a', 'b']
settime = ['Current shift', 'Today','This Week', 'A Week' ,'1 day shift', '1 night shift', 'Select time']
day_time = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']
schedule_set = []

#region 主要UI畫面
class MainWindow(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self._window = None
        self._counter = 100
        self.lastselect = None
        self.setup_ui()
        #self.now_time()
        self.Globol_var()
        
    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        loader = QUiLoader()
        file = QFile(r"C:\littleTooldata\IPLAS\program\loadi_ui.ui")
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()
        #self._window.installEventFilter(self)
        self.stage_change = 'none'

        self.get_schedular_data()
        self.now_time()
        self.set_date_start()
        self.set_date_end()
        self.set_calendar_start()
        self.set_calendar_end()
        self.Execute_btm()
        self.set_day_start_time()
        self.set_day_end_time()
        self.close_window()
        self.settime_selection()
        self.showinformation()
        self.set_show_current_status()
        self.project_selection()
        self.set_scheduler_time()
        self.stop_btm()
        self.check_box_1()
        self.check_box_fail()
        self.check_box_retest()
        self.check_box_disable()
        self.set_default_path()
        self.set_download_path_btm()
        self.refresh_project_btm()
        self.set_schedular_btm()
        self.delet_schedule_btm()
        self.set_download_path_todefult_btm()
        self.choose_schedular()
        self.mouse_click_event()
    
    #region 下拉式選單的顯示和連接
    #選擇project
    def project_selection(self):
        self.pro_selection = self._window.comboBox
        self.pro_selection.addItems(project)
        self.pro_selection.activated[str].connect(self.setinformation)
        self.pro_selection.setCurrentText(Select_project)
        
    #選擇時間
    def settime_selection(self):
        self.time_selection = self._window.comboBox_2
        self.time_selection.addItems(settime)
        self.time_selection.activated[str].connect(self.setdisable)
        self.time_selection.activated[str].connect(self.setinformation)
        self.time_selection.setCurrentText(Set_selecttime)

    #使用者自己選擇日期時間 -選擇開始日期(連結跳出式月曆)
    def set_date_start(self):
        self.date_start = self._window.dateEdit
        self.date_start.setEnabled(False)
        self.date_start.setDisplayFormat('yyyy/MM/dd')
        self.date_start.setDate(QDate.currentDate())
        self.date_start.setCalendarPopup(True)
        self.date_start.setCalendarWidget(self._window.calendarWidget)
        self.date_start.dateChanged.connect(self.setinformation)

    #使用者自己選擇日期時間 -選擇結束日期(連結跳出式月曆)  
    def set_date_end(self):
        self.date_end = self._window.dateEdit_2
        self.date_end.setEnabled(False)
        self.date_end.setDisplayFormat('yyyy/MM/dd')
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setCalendarPopup(True)
        self.date_end.setCalendarWidget(self._window.calendarWidget_2)
        self.date_end.dateChanged.connect(self.setinformation)

    #使用日曆選擇日期 (開始日期)
    def set_calendar_start(self):
        self.calendar_start = self._window.calendarWidget
        self.calendar_start.setGridVisible(True)
        self.calendar_start.setMinimumDate(QDate(2022, 1,1))
        self.calendar_start.setMaximumDate(QDate.currentDate())
        self.calendar_start.setFirstDayOfWeek(Qt.Monday)
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QBrush(Qt.gray, Qt.SolidPattern))

        self.calendar_start.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        self.calendar_start.setWeekdayTextFormat(Qt.Sunday, weekend_format)
        weekend_format.setForeground(QBrush(QColor('#8800BB'), Qt.SolidPattern))
        self.calendar_start.setDateTextFormat(QDate.currentDate(), weekend_format)
        self.calendar_start.clicked.connect(self.date_start.setDate)
    
    #使用日曆選擇日期 (結束日期)   
    def set_calendar_end(self):
        self.calendar_end = self._window.calendarWidget_2
        self.calendar_end.setGridVisible(True)
        self.calendar_end.setMinimumDate(QDate.currentDate().addMonths(-1))
        self.calendar_end.setMaximumDate(QDate.currentDate())
        self.calendar_end.setFirstDayOfWeek(Qt.Monday)
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QBrush(Qt.gray, Qt.SolidPattern))
        self.calendar_end.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        self.calendar_end.setWeekdayTextFormat(Qt.Sunday, weekend_format)
        weekend_format.setForeground(QBrush(QColor('#8800BB'), Qt.SolidPattern))
        self.calendar_end.setDateTextFormat(QDate.currentDate(), weekend_format)
        self.calendar_end.clicked.connect(self.date_end.setDate)

    #使用者自己選擇日期時間 - 選擇開始時間
    def set_day_start_time(self):
        self.day_start_time = self._window.comboBox_3
        self.day_start_time.addItems(day_time)
        self.day_start_time.setEnabled(False)
        self.day_start_time.activated.connect(self.setinformation)

    #使用者自己選擇日期時間 - 選擇結束時間  
    def set_day_end_time(self):
        self.day_end_time = self._window.comboBox_4
        self.day_end_time.addItems(day_time)
        self.day_end_time.setEnabled(False)
        self.default_time = str(self.now.hour) + ':00'
        self.day_end_time.setCurrentText(self.default_time)
        self.day_end_time.activated.connect(self.setinformation)
    
    #選擇排程時間
    def set_scheduler_time(self):
        self.schedular_time = self._window.timeEdit
        self.schedular_time.setDisplayFormat("HH:mm")
        self.schedular_time.setTime(QTime(int(Set_schedular_time.split(':')[0]),int(Set_schedular_time.split(':')[1])))
        self.schedular_time.timeChanged.connect(self.setinformation)
    
    #選擇排程
    def choose_schedular(self):
        self.schedular = self._window.comboBox_5
        self.schedular.addItems(schedule_set)
        self.schedular.setCurrentIndex(-1)
        self.schedular.activated[str].connect(self.showscheduleselection)
    #endregion

    #region 設定是否要下載retest_pass and fail選項
    def check_box_1(self):
        self.checkbox_setdiable = self._window.checkBox_3
        if check_box_default[0]:
            self.checkbox_setdiable.setChecked(True)
        else:
            self.checkbox_setdiable.setChecked(False)
        self.checkbox_setdiable.stateChanged.connect(self.check_box_disable)
    
    def check_box_retest(self):
        self.checkbox_retest = self._window.checkBox
        if check_box_default[1]:
            self.checkbox_retest.setChecked(True)
        else:
            self.checkbox_retest.setChecked(False)

    def check_box_fail(self):
        self.checkbox_fail = self._window.checkBox_2
        if check_box_default[2]:
            self.checkbox_fail.setChecked(True)
        else:
            self.checkbox_fail.setChecked(False)

    def check_box_disable(self):
        if self.checkbox_setdiable.isChecked():
            self.checkbox_fail.setChecked(True)
            self.checkbox_retest.setChecked(True)
            self.checkbox_retest.setEnabled(False)
            self.checkbox_fail.setEnabled(False)
        else:
            self.checkbox_retest.setEnabled(True)
            self.checkbox_fail.setEnabled(True)

    #endregion 

    #region 設定下載地址
    def set_default_path(self):
        self._window.lineEdit.setText(download_path)
    
    def set_download_path_btm(self):
        self._window.pushButton_8.clicked.connect(self.open_file)
    
    def open_file(self):
        self.folder_path = QFileDialog.getExistingDirectory(self._window, 'Open folder', './')
        self.folder_path = self.folder_path.replace("/", "\\")
        self._window.lineEdit.setText(self.folder_path)
    
    #endregion 

    #region 設置按鈕不能按    
    def setdisable(self, text):
        
        if text in ['Current shift', 'Today','This Week', 'A Week' ,'1 day shift', '1 night shift']:
            self.date_start.setEnabled(False)
            self.date_end.setEnabled(False)
            self.day_start_time.setEnabled(False)
            self.day_end_time.setEnabled(False)

        if text == 'Select time':
            self.date_start.setEnabled(True)
            self.date_end.setEnabled(True)
            self.day_start_time.setEnabled(True)
            self.day_end_time.setEnabled(True)
        
        if text == 'Start Downloading File':
            self.pro_selection.setEnabled(False)
            self.time_selection.setEnabled(False)
            self.date_start.setEnabled(False)
            self.date_end.setEnabled(False)
            self.day_start_time.setEnabled(False)
            self.day_end_time.setEnabled(False)
            self._window.pushButton.setEnabled(False)
            self._window.checkBox_3.setEnabled(False)
            self._window.checkBox.setEnabled(False)
            self._window.checkBox_2.setEnabled(False)
            self._window.pushButton_8.setEnabled(False)
            self._window.lineEdit.setEnabled(False)
            self._window.pushButton_4.setEnabled(False)
            self._window.timeEdit.setEnabled(False)
            self._window.pushButton_6.setEnabled(False)
            self._window.pushButton_7.setEnabled(False)
            self._window.comboBox_5.setEnabled(False)
            self._window.pushButton_3.setEnabled(True)

        if self.stage_change == 'stop' or text == 'Download completed' or 'Download Failed' in text:
            self.pro_selection.setEnabled(True)
            self.time_selection.setEnabled(True)
            self._window.pushButton.setEnabled(True)
            if self.time_selection.currentText() == 'Select time':
                self.date_start.setEnabled(True)
                self.date_end.setEnabled(True)
                self.day_start_time.setEnabled(True)
                self.day_end_time.setEnabled(True)
            self._window.checkBox_3.setEnabled(True)
            self.check_box_disable()
            self._window.pushButton_8.setEnabled(True)
            self._window.lineEdit.setEnabled(True)
            self._window.pushButton_8.setEnabled(True)
            self._window.lineEdit.setEnabled(True)
            self._window.pushButton_4.setEnabled(True)
            self._window.timeEdit.setEnabled(True)
            self._window.pushButton_6.setEnabled(True)
            self._window.pushButton_7.setEnabled(True)
            self._window.comboBox_5.setEnabled(True)
            self._window.pushButton_3.setEnabled(False)

        
        
        #endregion

    #region 顯示初始資訊&字體設定
    def showinformation(self):
        self.now_time()
        self.show_info = self._window.plainTextEdit
        self.show_info.setReadOnly(True)
        self.cursor = self.show_info.textCursor()
        self.show_info.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.show_info.clear()
        self.space = '     '
        
        self.information =  ['Select Project : ',
                        'Set Time : ',
                        'Set Task Scheduler Time : ',
                        '============================']

        fft1 = self.show_info.currentCharFormat()
        fft1.setForeground(Qt.darkBlue)
        fft1.setFontWeight(QFont.Bold)
        fft2 = self.show_info.currentCharFormat()
        fft2.setForeground(Qt.black)
        fft2.setFontWeight(QFont.Normal)
        
        self.show_info.setCurrentCharFormat(fft1)
        self.show_info.appendPlainText(self.information[0])
        self.show_info.setCurrentCharFormat(fft2)
        self.show_info.appendPlainText(self.space + Select_project)
        self.show_info.setCurrentCharFormat(fft1)
        self.show_info.appendPlainText(self.information[1])
        self.show_info.setCurrentCharFormat(fft2)
        information_index, tempset = self.get_tempset(Set_selecttime)
        self.show_info.appendPlainText(self.space + tempset)
        self.show_info.setCurrentCharFormat(fft1)
        self.show_info.appendPlainText(self.information[2])
        self.show_info.setCurrentCharFormat(fft2)
        self.show_info.appendPlainText(self.space + Set_schedular_time)
        self.show_info.setCurrentCharFormat(fft2)
        self.show_info.appendPlainText(self.information[3])
       
        for i in schedule_set:
            #self.show_info.setCurrentCharFormat(fft3)
            self.show_info.appendPlainText(i)
        self.show_info.moveCursor(QTextCursor.Start)
        
    def mouse_click_event(self):
        self.show_info.mousePressEvent = self.mouse_click_position
    
    def mouse_click_position(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(f'(x,y) = ({x},{y})')

    #設定執行狀態顯示字體
    def set_show_current_status(self):
        self.now_time()
        self.show_current = self._window.plainTextEdit_2
        self.cursor_show = self.show_current.textCursor()
        self.show_current.setReadOnly(True)
        self.show_current.setStyleSheet("background : black")
        #self.show_current.setFocus()
        self.stagespace = '  '
        self.exefont = self.show_current.currentCharFormat()
        
        self.exefont.setForeground(Qt.green)
        self.exefont.setFontWeight(QFont.Normal)
        self.exefont.setFontPointSize(10)
        self.show_current.moveCursor(QTextCursor.End)
        self.show_current.setCurrentCharFormat(self.exefont)
    
    #顯示下方狀態字幕
    def show_current_status(self, text):
        self.current_show = self.show_current.toPlainText()
        self.cursor_show.clearSelection() 
        self.show_current.appendPlainText(self.now_H_M + self.stagespace + text)
              
    #endregion

    def get_schedular_data(self):
        os.chdir(schedule_data_path)
        for file in glob.glob("*.bat"):
            file = file.split('.')[0]
            file = file.replace("-", ":")
            schedule_set.append(file)
        #print(schedule_set)

    #region 當按鈕改變時改變顯示的資訊
    def setinformation(self, get):
        self.current = self.show_info.toPlainText()
        self.cursor.clearSelection()
        self.show_info.moveCursor(QTextCursor.Start)
        fmt = QTextCharFormat()
        fmt.setForeground(Qt.black)
        fmt.setFontWeight(QFont.Normal)
        #self.show_info.setFocus()
        information_index, tempset = self.get_tempset(get)
        words = self.current.find(self.information[information_index]) #找到想找的字的第一個字母位置
        position = words + len(self.information[information_index])
        self.cursor.setPosition(position)  #移動光標到想找的字母之後
        next_position = self.current.find(self.information[information_index+1])
        self.cursor.setPosition(next_position, QTextCursor.KeepAnchor) #移動錨點到這行最後面(選擇冒號到最後面這之間的文字)
        if self.cursor.hasSelection():                        #如果有東西，那就刪除文字，插入新的文字
            self.cursor.removeSelectedText()
        self.cursor.insertBlock()
        self.cursor.insertText(self.space + tempset + '\n', fmt) 
    #endregion

    def showscheduleselection(self, get):
        fmt2 = QTextCharFormat()
        fmt2.setForeground(Qt.black)
        fmt2.setFontWeight(QFont.Normal)
        fmt2.setBackground(Qt.yellow)
        
        fmt = QTextCharFormat()
        fmt.setForeground(Qt.black)
        fmt.setFontWeight(QFont.Normal)

        self.current = self.show_info.toPlainText()
        self.cursor.clearSelection()
        if self.lastselect != None:
            start_index = self.current.find(self.lastselect)
            end_index = start_index + len(self.lastselect)
            self.cursor.setPosition(start_index)
            self.cursor.setPosition(end_index, QTextCursor.KeepAnchor)
            if self.cursor.hasSelection():                       
                self.cursor.removeSelectedText()
            self.cursor.insertText(self.lastselect, fmt)    

        start_index = self.current.find(get)
        end_index = start_index + len(get)
        self.cursor.setPosition(start_index)
        self.cursor.setPosition(end_index, QTextCursor.KeepAnchor)
        if self.cursor.hasSelection():                        
            self.cursor.removeSelectedText()
        self.cursor.insertText(get, fmt2)
        self.lastselect = get
    
    def removescheduleselection(self):
        start_index = self.current.find(self.lastselect)
        end_index = start_index + len(self.lastselect)
        self.cursor.setPosition(start_index)
        self.cursor.setPosition(end_index, QTextCursor.KeepAnchor)
        if self.cursor.hasSelection():                        
            self.cursor.removeSelectedText()
            self.cursor.deletePreviousChar()
        self.lastselect = None
    
    def addsheduleset(self, text):
        fft2 = self.show_info.currentCharFormat()
        fft2.setForeground(Qt.black)
        fft2.setFontWeight(QFont.Normal)

        text = text.split('.')[0].replace('-', ":")
        schedule_set.append(text)
        self.show_info.moveCursor(QTextCursor.End)
        self.show_info.setCurrentCharFormat(fft2)
        self.show_info.appendPlainText(text)
        self.current = self.show_info.toPlainText()
        self.cursor.clearSelection()
        self.show_info.moveCursor(QTextCursor.StartOfLine)
        
        self.schedular.clear()
        self.schedular.addItems(schedule_set)
        self.schedular.setCurrentIndex(-1)
        
    #region 得到使用者即時選擇的資訊並且傳回給顯示面板
    def get_tempset(self, text):
        self.now_time()   #更新最新時間
        information_index = 0
        tempset = ''
        if text in project:       #使用者選擇project時
            information_index = 0
            tempset = text
        #settime = ['Current shift', 'Today', 'This Week', 'A Week' ,'1 day shift', '1 night shift']
        if text in settime[:-1]:
            information_index = 1
            #Current shift 今日早上8點到現在時間
            if text == settime[0]:                     
                tempset = self.nowdate + ' 08:00' + ' ~' + '\n' + self.space + self.nowdatetime
            #Today 今日0點到現在時間
            if text == settime[1]:                      
                tempset = self.nowdate + ' 00:00' + ' ~' + '\n' + self.space + self.nowdatetime
            #This Week 這禮拜一 0點 到 現在時間點
            if text == settime[2]:                      
                delta = datetime.timedelta(days = datetime.datetime.today().weekday())
                thisweek = self.now - delta
                thisweek_date = thisweek.strftime('%Y/%m/%d')
                tempset = thisweek_date + ' 00:00' + ' ~' + '\n' + self.space + self.nowdatetime
            #A Week 一個禮拜
            if text == settime[3]:                      
                lastweek = self.now - datetime.timedelta(weeks = 1)
                lastweek_datetime = lastweek.strftime('%Y/%m/%d')
                tempset = lastweek_datetime + ' 00:00' + ' ~' + '\n' + self.space + self.nowdatetime
            #1 day shift  昨天8點 到 現在時間點
            if text == settime[4]:                    
                delta = datetime.timedelta(days = 1)
                yesterday = self.now - delta
                yesterday_date = yesterday.strftime('%Y/%m/%d')
                tempset = yesterday_date + ' 08:00' + ' ~' + '\n' + self.space + self.nowdate + ' 20:00' 
            #1 night shift 過一晚上，昨天下班(晚上8點) 到 現在時間點
            if text == settime[5]:  
                delta = datetime.timedelta(days = 1)
                yesterday = self.now - delta
                yesterday_date = yesterday.strftime('%Y/%m/%d')                   
                tempset = yesterday_date + ' 20:00' + ' ~' + '\n' + self.space + self.nowdate + ' 08:00'
        
        #如果text為使用這自己選擇的日期時間(當text為'Select time' 或是 他的type為數字(選擇時間) 或是 他的type為QtCore.QDate(使用日曆選擇時間))
        if  text == 'Select time' or type(text) == int or type(text) == QtCore.QDate:     
            information_index = 1
            tempset = self.date_start.date().toString('yyyy/MM/dd') + ' ' + self.day_start_time.currentText() + ' ~' + '\n' + self.space + self.date_end.date().toString('yyyy/MM/dd')+ ' ' +  self.day_end_time.currentText()
       
        #如果text為使用者改變排程日期時
        if  type(text) == QtCore.QTime:       
            information_index = 2
            temp = self.schedular_time.time().toString()
            tempset = temp.split(':')[0] + ':' + temp.split(':')[1]
    
        return information_index, tempset  
        #endregion 
                    
    #region 訊號設定   
    #def change_execute(self):
        #self.stage_change = 'execute'
    
    def change_stop(self):
        self.stage_change = 'stop'
    
    def change_none(self):
        self.stage_change == 'none'
    #endregion 

    #region 通用參數設定
    def now_time(self):     
        self.now = datetime.datetime.now()   #2022-05-01 11:22:30.000 type = <class 'datetime.datetime'> 可以做日期相減
        self.nowdatetime = self.now.strftime('%Y/%m/%d %H:%M')   #轉換成str格式
        self.nowdate = self.now.strftime('%Y/%m/%d') #得到現在的 年 月 日  
        self.now_H_M = self.now.strftime('%H:%M')  #得到 小時:分鐘 ex: 20:30 (顯示現在狀態前面時間用)
                 
    def Globol_var(self):
        self.temp_project = self.pro_selection.currentText()    #得到即時的使用者選擇的專案
        self.temp_selecttime = self.time_selection.currentText()    #得到即時的使用者選擇的時間
        information_index, tempset = self.get_tempset(self.time_selection.currentText())
        self.temp_timeperiod = tempset
        
        self.check_box_temp = [1, 1, 1]                            #得到即時的使用者選擇的下載選項
        if not self.checkbox_setdiable.isChecked():
            self.check_box_temp[0] =0
        if not self.checkbox_retest.isChecked():
            self.check_box_temp[1] =0
        if not self.checkbox_fail.isChecked():
            self.check_box_temp[2] =0

        self.temp_download_path = self._window.lineEdit.text()              #得到即時的使用者選擇的下載位址
        self.temp_arrang = self.schedular_time.time().toString('HH:mm')        #得到即時的使用者選擇的排程時間
    #endregion
 
    #region設定執行參數
    def execute_data(self):
        self.Globol_var()  #更新現在面板上的最新參數
        global execute_dict
        
        execut_project = [self.temp_project, project.index(self.temp_project)]
        execute_time = [self.temp_selecttime, settime.index(self.temp_selecttime), self.temp_timeperiod]
        execute_dict = {"All_project" : project,
                        "Select_project" : execut_project,
                        "Time_set" :  execute_time,
                        "Check_box_default" :  self.check_box_temp,
                        "Download_path" : self.temp_download_path,
                        'Set_schedular_time' : self.temp_arrang
                        }
        #print(execute_dict)
    #endregion
    
    #region 設定按鈕行為
    #執行按鈕
    def Execute_btm(self):
        self._window.pushButton.clicked.connect(self.check_datetime_and_excute) 
        self._window.pushButton.clicked.connect(self.change_none) 
    #設為預設按鈕
    #def setDefault_btm(self):
        #self._window.pushButton_5.clicked.connect(self.write_to_defaultfile)    #寫入檔案中
                
    #回到預設按鈕
    #def return_to_default_btm(self):
        #self._window.pushButton_4.clicked.connect(self.showinformation)
        #self._window.pushButton_4.clicked.connect(self.return_to_default)

    #停止按鈕 停止下載
    def stop_btm(self):
        self._window.pushButton_3.clicked.connect(self.change_stop)
        self._window.pushButton_3.clicked.connect(self.setdisable)
        self._window.pushButton_3.clicked.connect(self.stop_download)
    
    def set_download_path_todefult_btm(self):
        self._window.pushButton_4.clicked.connect(self.download_path_setup)

    #更新使用者project
    def refresh_project_btm(self):
        self._window.pushButton_9.clicked.connect(self.start_refresh_thread)   

    #排程按鈕設定
    def set_schedular_btm(self):
        self._window.pushButton_6.clicked.connect(self.set_schedular)
    
    def delet_schedule_btm(self):
        self._window.pushButton_7.clicked.connect(self.del_schedular)
        
    #endregion 
    

    def stop_download(self):
        #start_download_thread.stop(self)
        Download_isn.stop_download_file(stop = "stop")
        self.show_current_status("Stop Progress!")
        self.excute_thread.quit()    

    #region更新使用者project 相關函式
    def reload_project_combo(self):
        self.pro_selection.clear()
        self.pro_selection.addItems(project)
        self.show_current_status('Update Project Completed!')

    def start_refresh_thread(self):
        self.get_refresh_thread = getproject_thread()
        self.get_refresh_thread.signal.connect(self.write_to_defaultfile)
        self.get_refresh_thread.start()
        self.show_current_status("Start Getting User Project...")
    
    def set_schedular(self):
        self.execute_data()
        if (settime.index(self.temp_selecttime)) == 6:
            self.errobox('行程不能為特定時間')
        else:
            filename, text = write_set_schedular.set_scheduler(execute_dict)
            if filename != None:
                self.addsheduleset(filename)
            self.show_current_status(text)
    
    def del_schedular(self):
        self.currentselectschedule = self.schedular.currentText()
        self.currentselectschedule = self.currentselectschedule.replace(":", "-")
        self.currentselectschedule = self.currentselectschedule + ".bat"
        text = write_set_schedular.del_scheduler(self.currentselectschedule)
        self.removescheduleselection()
        self.show_current_status(text)
        schedule_set.remove(self.schedular.currentText())
        self.schedular.clear()
        self.schedular.addItems(schedule_set)
        self.schedular.setCurrentIndex(-1)
        

    def download_path_setup(self):
        global download_path
        download_path = self._window.lineEdit.text()
        self.write_to_defaultfile('')
    #endregion

    #回到預設        
    ''' def return_to_default(self):
        self.pro_selection.setCurrentText(Select_project)
        self.time_selection.setCurrentText(Set_selecttime)
        self.schedular_time.setTime(QTime(int(Set_schedular_time.split(':')[0]),int(Set_schedular_time.split(':')[1])))
        self.setdisable(Set_selecttime)
        self.check_box_1()
        self.check_box_retest()
        self.check_box_fail()
        self.set_default_path()
        self.show_current_status('Return to Default Set') '''

    #寫入預設檔案
    def write_to_defaultfile(self, signal):
        data = { 'All_project' : project, 
                 'Select_project' : [project[0], 0],
                 'Time_set' : [settime[0], 0],
                 'Check_box_default' : [1 ,1 ,1],
                 'Download_path' : download_path,
                 'Set_schedular_time' : '09:30'
            }
        file_util.write_json(IPLAS_defaultset_path, data)
        load_initset()
            
        IPLAS_UI_logger.info(f"write_to_default : Select_project : {Select_project}\nSet_selecttime : {Set_selecttime}\ncheck_box_default : {check_box_default}\ndownload_path : {download_path}")           #從檔案中讀取剛剛存取的設定並且導
        #print('\nSelect_project : ', Select_project,
            #'\nSet_selecttime : ', Set_selecttime,   
            #'\nheck_box_default : ',check_box_default,
            #'\ndownload_path : ', download_path)

        if signal == "finish":
            self.reload_project_combo()
        self.show_current_status('Set Default File Done!')
           
        

    #檢查時間並且執行        
    def check_datetime_and_excute(self):
        start_time = self.date_start.date().toString(Qt.ISODate) + ' ' + self.day_start_time.currentText() + ':00'
        end_time = self.date_end.date().toString(Qt.ISODate)+ ' ' + self.day_end_time.currentText() + ':00'
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        
        if check_internet():
            if start > self.now or end > self.now:
                self.errobox('不能超過現在時間!')
                
            elif end < start:
                self.errobox('結束時間不能在起始時間之前!')
                
            elif abs(end-start).days >= 30:
                self.errobox('時間間格不能大於一個月!')
            
            else:
                self.setdisable(text = 'Start Downloading File')
                self.show_current.clear()
                self.execute_data()
                IPLAS_UI_logger.info(f"execute_dict : {execute_dict}")
                #print(execute_dict)
                self.start_download_thread()
        else:
            self.errobox("沒網路連接!")
           

    #錯誤視窗
    def errobox(self, text):
        QMessageBox.warning(self._window, 'error', text, QMessageBox.Ok)
    
    def start_download_thread(self):
        self.excute_thread = start_download_thread()
        self.excute_thread.status.connect(self.show_current_status)
        self.excute_thread.status.connect(self.setdisable)
        self.excute_thread.start()
    
    def close_window(self):
        self._window.pushButton_3.clicked.connect(self.stop_download)
        self._window.pushButton_2.clicked.connect(self.exit)

    @QtCore.Slot()
    def exit(self):
        self._window.close()

#endregion
    
#region 設定初始值
def load_initset():
    global project
    global Select_project
    global Set_selecttime
    global Set_schedular_time
    global check_box_default
    global download_path
    del project[:]
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(IPLAS_data_path):
        os.makedirs(IPLAS_data_path) 
    if not os.path.exists(IPLAS_defaultset_path) or os.path.getsize(IPLAS_defaultset_path) == 0:
        run_getproject()
        data = { 'All_project' : project, 
                 'Select_project' : [project[0], 0],
                 'Time_set' : [settime[0], 0],
                 'Check_box_default' : [1 ,1 ,1],
                 'Download_path' : download_path,
                 'Set_schedular_time' : '09:30'
        }
        file_util.write_json(IPLAS_defaultset_path, data)
    data = file_util.read_json(IPLAS_defaultset_path)
    project = data['All_project']
    Select_project = data['Select_project'][0]
    Set_selecttime = data['Time_set'][0]
    check_box_default = data['Check_box_default']
    download_path = data['Download_path']
    Set_schedular_time = data['Set_schedular_time']
#endregion

#region 初始化chrome driver

def get_chrome_driver():
    driver_path = chromedriver_helper.return_driver_path()
    s = Service(driver_path)
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  
    options.add_argument("--headless")
    driver = webdriver.Chrome(service = s, options = options)
    return driver

#endregion

class start_download_thread(QThread):
    status = Signal(str)
    def __init__(self):
        QThread.__init__(self)
    
    def run(self):
        Download_isn.run(execute_dict = execute_dict, self = self, status =  self.status)
    
    def stop(self):
        Download_isn.stop_download_file(stop = "stop")


#region 擷取使用者所擁有的project，並寫入project變數裡面
def run_getproject():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    mainwindow = Getproject()
    mainwindow.show()
    app.exec_()

'''去IPLAS擷取使用者的所有project'''
class getproject_thread(QThread):
    signal = Signal(str)
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        del project[:]
        driver = get_chrome_driver()
        driver.get(IPLAS_url)
        try:
            wait = WebDriverWait(driver, 60)
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type = 'text']")))
        except Exception:
            IPLAS_UI_logger.exception("fail to load IPLAS")
        else:
            driver.find_element(by=By.CSS_SELECTOR, value="input[type = 'text']").send_keys(password[0])
            driver.find_element(by=By.CSS_SELECTOR, value="input[type = 'password']").send_keys(password[1])
            driver.find_element(by=By.CSS_SELECTOR, value=".btn.btn-default.pega_login.ldaplogin").click()
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".container.pega_home_page")))
            project_row = driver.find_elements(by=By.CSS_SELECTOR, value="li[class^='js-prj']")
            length=len(project_row)
            for i in range(length):   
                project.append(project_row[i].get_attribute("innerText"))
            driver.quit()
            IPLAS_UI_logger.info("Success get user project")
            self.signal.emit("finish")


'''創一個小視窗並顯示等待字樣'''
class Getproject(QMainWindow):
    signal = Signal(int)
    def __init__(self):
        super(Getproject, self).__init__()
        self.init_UI()
        self.startproject()
        self.startthread()

    def init_UI(self):
        self.setWindowTitle("stage")
        self.setGeometry(500,500,350,150)

        self.label = QLabel(self)
        font = QFont("Arial", 14, QFont.Bold)
        self.label.setFont(font)
        self.label.setGeometry(30,15,300,100)
        
    def startthread(self):
        self.work = loadingThread()
        self.work.start()
        self.work.trigger.connect(self.updatelabel)
        self.work.setTerminationEnabled(True)
        self.updatelabel('...')
    
    def startproject(self):
        self.get_thread = getproject_thread()
        self.get_thread.signal.connect(self.done)
        self.get_thread.start()

    def updatelabel(self, text):
        self.label.setText('Catch User Project  ' + text) 

    def done(self):
        self.close()  

'''字後面的小動畫'''
class loadingThread(QThread):
    trigger = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.dot = ['.','..', '...']

    def run(self):
        while True :
            for i in self.dot:
                time.sleep(0.3)
                self.trigger.emit(i) 

#endregion 


def check_internet():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    proxies = {"http":"proxy8.intra:80"}
    auth = HttpNtlmAuth(password[0], password[1])
    url = 'http://eip.tw.pegatroncorp.com/'
    try :
        resp = requests.get(url = url,headers = headers, proxies=proxies, auth = auth, timeout=300)
    except Exception:
        IPLAS_UI_logger.exception("Internet connect failed")
        return False
    else:
        return True


if '__main__' == __name__:
    #reset_defaultset()
    load_initset()
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.window.show()

    ret = app.exec_()
    sys.exit(ret)
 