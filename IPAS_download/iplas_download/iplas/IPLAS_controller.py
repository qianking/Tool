from logging import exception
import sys
from datetime import datetime, timedelta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QFile, QThread, Signal, Qt, QRunnable, QThreadPool, QObject, QDate, QTime, QPoint, QTimer
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QMainWindow, QCalendarWidget
from PySide6.QtGui import QFont, QColor, QIntValidator, QTextCharFormat, QBrush, QTextCursor
from IPLAS_UI import Ui_MainWindow
import tests.test_2

VERSION = '1.0.1'

download_path = r'D:\download'
project = ['SWITCH_CISCO_EZ1KA1', 'b']
time_selection = ['Current shift', 'Today','This Week', 'A Week' ,'1 day shift', '1 night shift', 'Select time']
day_time = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']


schedule_set = ['09:00 SWITCH_CISCO_EZ1KA1(Current shift)', '09:15 SWITCH_CISCO_EZ1KA1(Today)', '10:00 SWITCH_CISCO_EZ1KA1(A Week)']

class MainWindow(QMainWindow):
    def __init__(self, UI_file_format, parent=None):
        super(MainWindow, self).__init__()
        self.UI_file_format = UI_file_format
        if UI_file_format == 'py':
            self._window = Ui_MainWindow()
            self._window.setupUi(self)
        elif UI_file_format == 'ui':
            self._window = None

        self._count_timer = QTimer(self)
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.execute_flag = True

        self.setup_ui()
        self.last_cursor = None
        self.last_info = str()
        self.show_info.mousePressEvent = self.hightlight_selection
        self.show_info.keyPressEvent = self.open_delete_key
        self.show_info.mouseMoveEvent = self.change_mouse_shape
        

    @property
    def window(self):
        return self._window
    
    def setup_ui(self):
        if self.UI_file_format == 'ui':
            loader = QUiLoader()
            file = QFile('./IPLAS_ui.ui')
            file.open(QFile.ReadOnly)
            self._window = loader.load(file)
            file.close()
        self.set_window_title()
        if self.UI_file_format == 'ui':
            self._window.installEventFilter(self)
        
        self.get_now_time()
        self.set_project_group()
        self.project_selection()
        self.refresh_project_btm()
        self.set_time_group()
        self.settime_selection()
        self.set_date_start()
        self.set_date_end()
        self.set_day_start_time()
        self.set_day_end_time()
        self.set_schedule_group()
        self.set_scheduler_time()
        self.set_schedular_btm()
        self.del_schedular_btm()
        self.set_download_path_group()
        self.set_default_path()
        self.set_download_path_btm()
        self.setup_info()
        self.set_show_current_status()
        self.Execute_btm()
        self.Stop_btm()
        self.Exit_btm()
        
        
    #監看是否有關掉視窗的事件觸發 .ui版本
    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
        if (watched is self._window) and (event.type() == QtCore.QEvent.Close):
            reply = QMessageBox.question(self, 'Warning', 'sure?', QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()
                return True
        return super().eventFilter(watched, event)

    ''' #監看是否有關掉視窗的事件觸發 .py版本
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', 'sure?', QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()
            return True
        return super().closeEvent(event) '''

    
    def set_window_title(self):
        if UI_file_format == 'ui':
            self._window.setWindowTitle(f'IPLAS Download V{VERSION}')    #.ui版本
        else:
            self.setWindowTitle(f'IPLAS Download V{VERSION}')             #.py版本

    def get_now_time(self):     
        self.now = datetime.now()   #2022-05-01 11:22:30.000 type = <class 'datetime.datetime'> 可以做日期相減
        self.nowdatetime = str(self.now.strftime('%Y/%m/%d %H:%M'))   #得到現在的 年/月/日 時/分
        self.nowdate = str(self.now.strftime('%Y/%m/%d')) #得到現在的 年/月/日
        self.now_H = str(self.now.strftime('%H')) #得到現在的 時
        self.now_H_M = str(self.now.strftime('%H:%M'))  #得到 時:分 ex: 20:30 (顯示現在狀態前面時間用)

#region 設置項目選擇
    def set_project_group(self):
        self.groupBox = self._window.groupBox
        self.groupBox.setTitle('選擇項目')
        self.groupBox.setFont(QFont('Arial', 13))

    #選擇project
    def project_selection(self):
        self.pro_selection = self._window.comboBox
        self.pro_selection.setFont(QFont('Calibri', 13))
        self.pro_selection.setFixedWidth(330)
        self.pro_selection.addItems(project)
        self.pro_selection.currentTextChanged.connect(self.change_info_show)
        self.pro_selection.setCurrentText(project[0])
    
    #更新使用者project
    def refresh_project_btm(self):
        self.refresh = self._window.pushButton_9
        self.refresh.setFixedWidth(30)
        self.refresh.setFixedHeight(30)
        self.refresh.setFont(QFont('Calibri', 13))
        self.refresh.setLayoutDirection(Qt.RightToLeft)
        #self.refresh.clicked.connect(self.start_refresh_thread)
#endregion
    
#region 設置時間選擇
    def set_time_group(self):
        self.groupBox_2 = self._window.groupBox_2
        self.groupBox_2.setTitle('選擇時間')
        self.groupBox_2.setFont(QFont('Arial', 13))

    #選擇時間
    def settime_selection(self):
        self.time_selection = self._window.comboBox_2
        self.time_selection.addItems(time_selection)
        self.time_selection.setFont(QFont('Arial', 13))
        self.time_selection.currentTextChanged.connect(self.setdisable)
        self.time_selection.currentTextChanged.connect(self.change_info_show)
        self.time_selection.setCurrentText(time_selection[0])


    #使用者自己選擇日期時間 -選擇開始日期(連結跳出式月曆)
    def set_date_start(self):
        self.date_start = self._window.dateEdit
        self.date_start.setEnabled(False)
        self.date_start.setDisplayFormat('yyyy/MM/dd')
        self.date_start.setFont(QFont('Calibri', 13))
        self.date_start.setDate(QDate.currentDate())
        self.date_start.setCalendarPopup(True)
        self.date_start.dateChanged.connect(self.selecttime_change)
    
    #使用者自己選擇日期時間 -選擇結束日期(連結跳出式月曆)  
    def set_date_end(self):
        self.date_end = self._window.dateEdit_2
        self.date_end.setEnabled(False)
        self.date_end.setDisplayFormat('yyyy/MM/dd')
        self.date_end.setFont(QFont('Calibri', 13))
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setCalendarPopup(True)
        self.date_end.dateChanged.connect(self.selecttime_change)
    
    #使用者自己選擇日期時間 - 選擇開始時間
    def set_day_start_time(self):
        self.day_start_time = self._window.comboBox_3
        self.day_start_time.setEnabled(False)
        self.day_start_time.addItems(day_time)
        self.day_start_time.setCurrentIndex(0)
        self.day_start_time.setFont(QFont('Calibri', 13))
        self.day_start_time.activated.connect(self.selecttime_change)

    #使用者自己選擇日期時間 - 選擇結束時間  
    def set_day_end_time(self):
        self.day_end_time = self._window.comboBox_5
        self.day_end_time.setEnabled(False)
        self.day_end_time.addItems(day_time)
        now_hour = f"{self.now_H}:00"
        index = self.day_end_time.findText(now_hour, Qt.MatchFixedString)
        if index >= 0:
            self.day_end_time.setCurrentIndex(index) 
        self.day_end_time.setFont(QFont('Calibri', 13))
        self.day_end_time.activated.connect(self.selecttime_change)
#endregion
    def selecttime_change(self, txt):
        txt = 'selecttime_change'
        self.change_info_show(txt)
    
#region 設置排程
    def set_schedule_group(self):
        self.groupBox_4 = self._window.groupBox_4
        self.groupBox_4.setTitle('設定排程 (單次執行不用設定)')
        self.groupBox_4.setFont(QFont('Arial', 13))
    
    def set_scheduler_time(self):
        self.schedular_time = self._window.timeEdit
        self.schedular_time.setDisplayFormat("HH:mm")
        self.schedular_time.setTime(QTime(9,0))
        self.schedular_time.setFont(QFont('Calibri', 13))
        self.schedular_time.setFixedWidth(100)
        self.schedular_time.timeChanged.connect(self.change_info_show)
    
    def set_schedular_btm(self):
        self.set_schedular = self._window.pushButton_6
    
    def del_schedular_btm(self):
        self.del_schedular = self._window.pushButton_7
        self.del_schedular.clicked.connect(self.del_schedular_set)

#endregion
    
#region 設置下載路徑
    def set_download_path_group(self):
        self.groupBox_3 = self._window.groupBox_3
        self.groupBox_3.setTitle('設定下載地址')
        self.groupBox_3.setFont(QFont('Arial', 13))
    
    def set_default_path(self):
        self.download_path = self._window.lineEdit
        self.download_path.setText(download_path)
        self.download_path.setFont(QFont('Calibri', 13))
    
    def set_download_path_btm(self):
        self.select_download_path = self._window.pushButton_8
        self.select_download_path.clicked.connect(self.open_file)
    
    def open_file(self):
        global download_path
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Choose folder', './')
        if self.folder_path != download_path and self.folder_path != '':
            if len(self.folder_path.split('/')) >= 3:
                self.errobox('建議選擇路徑不要超過兩層，會有檔案開不起來的問題')
            else:
                self.folder_path = self.folder_path.replace("/", "\\")
                self.download_path.setText(self.folder_path)
                download_path = self.folder_path
            
#endregion    

    def setdisable(self, text):
        if text != 'Select time':
            self.date_start.setEnabled(False)
            self.date_end.setEnabled(False)
            self.day_start_time.setEnabled(False)
            self.day_end_time.setEnabled(False)
        else:
            self.date_start.setEnabled(True)
            self.date_end.setEnabled(True)
            self.day_start_time.setEnabled(True)
            self.day_end_time.setEnabled(True)
    
    def execute_disable(self):
        self.pro_selection.setEnabled(False)
        self.refresh.setEnabled(False)
        self.time_selection.setEnabled(False)
        self.date_start.setEnabled(False)
        self.date_end.setEnabled(False)
        self.day_start_time.setEnabled(False)
        self.day_end_time.setEnabled(False)
        self.download_path.setEnabled(False)
        self.select_download_path.setEnabled(False)
        self.schedular_time.setEnabled(False)
        self.set_schedular.setEnabled(False)
        self.del_schedular.setEnabled(False)
        self.execute.setEnabled(False)

    #region 顯示初始資訊&字體設定
    def setup_info(self):
        self.get_now_time()
        self.show_info = self._window.plainTextEdit
        self.show_info.setMouseTracking(True)
        #self.show_info.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        #self.show_info.setFixedWidth(400)
        self.show_info.setReadOnly(True)
        self._cursor = self.show_info.textCursor()
        self.show_info.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.show_info.clear()
        self.title_space = ' '*3
        self.inner_space = ' '*10

        self.information =  ['Excute Parameter:',
                        'Select Project:',
                        'Set Time:',
                        '==========================================', 
                        'Scheduler Setting:',
                        'Set Task Scheduler Time:',
                        'Scheduler Task information:',
                        ]

        self.title_font = self.show_info.currentCharFormat()
        self.title_font.setForeground(Qt.darkGreen)
        self.title_font.setFont(QFont('Arial', 12))
        #self.title_font.setFontWeight(QFont.Bold)
        
        self.second_title_font = self.show_info.currentCharFormat()
        self.second_title_font.setForeground(Qt.darkBlue)
        self.second_title_font.setFont(QFont('Arial', 12))
        self.second_title_font.setFontWeight(QFont.Bold)
        
        self.inner_font = self.show_info.currentCharFormat()
        self.inner_font.setForeground(Qt.black)
        self.inner_font.setFontWeight(QFont.Normal)
        self.inner_font.setFont(QFont('Arial', 11))
        
        self.show_info.setCurrentCharFormat(self.title_font)
        self.show_info.appendPlainText(self.information[0])

        self.show_info.setCurrentCharFormat(self.second_title_font)
        self.show_info.appendPlainText(self.title_space + self.information[1])
        self.show_info.setCurrentCharFormat(self.inner_font)
        self.show_info.appendPlainText(self.inner_space)
        self.show_info.setCurrentCharFormat(self.second_title_font)
        self.show_info.appendPlainText(self.title_space + self.information[2])
        self.show_info.setCurrentCharFormat(self.inner_font)
        information_index, tempset = self.get_real_info(time_selection[0])
        self.show_info.appendPlainText(self.inner_space + tempset)
        self.show_info.setCurrentCharFormat(self.inner_font)
        self.show_info.appendPlainText(self.information[3])

        self.show_info.setCurrentCharFormat(self.title_font)
        self.show_info.appendPlainText(self.information[4])
        self.show_info.setCurrentCharFormat(self.second_title_font)
        self.show_info.appendPlainText(self.title_space + self.information[5])
        self.show_info.setCurrentCharFormat(self.inner_font)
        self.show_info.appendPlainText(self.inner_space + '09:00')
        self.show_info.setCurrentCharFormat(self.second_title_font)
        self.show_info.appendPlainText(self.title_space + self.information[6])
        
        for i in schedule_set:
            self.show_info.setCurrentCharFormat(self.inner_font)
            self.show_info.appendPlainText(self.inner_space + i)
        self.show_info.moveCursor(QTextCursor.Start)
    #endregion


    #region 當按鈕改變時改變顯示的資訊
    def change_info_show(self, get):
        #print(get)
        self.current = self.show_info.toPlainText()
        self._cursor.clearSelection()
        #self.show_info.moveCursor(QTextCursor.Start)
      
        information_index, self.info = self.get_real_info(get)
        words = self.current.find(self.information[information_index]) #找到想找的字的第一個字母位置
    
        self._cursor.setPosition(words)  #移動光標到找到的標題
        self._cursor.movePosition(QTextCursor.Down) #移動光標下移一列
        self._cursor.movePosition(QTextCursor.StartOfLine) #移動光標到該列的最一開始
        start = self._cursor.position() #儲存起始位置
        line_of_info = len(self.info.split('\n')) #得到需要置換的資訊有幾行
        #print(self.info)
        for i in range(line_of_info-1):
            self._cursor.movePosition(QTextCursor.Down) 
        self._cursor.movePosition(QTextCursor.EndOfLine)
        end = self._cursor.position() #儲存結束位置
        self._cursor.setPosition(start)
        self._cursor.setPosition(end, QTextCursor.KeepAnchor) #選取需要置換的區域
        self._cursor.insertText(self.inner_space + self.info, self.inner_font)
        self.changing_flash()
    #endregion

    def changing_flash(self):
        self.compare_different()
        #print(self.diff_info)
        for i in range(1):
            QTimer.singleShot(100 + i * 200, self.light_font)
            QTimer.singleShot(200 + i * 200, self.normal_font)
    
    def compare_different(self):
        self.diff_info = list()
        tmp_list = [self.last_info, self.info]
        last_info_list = list()
        info_list = list()
        tmp_2_list = [last_info_list, info_list]
        if self.last_info != self.info:
            for num, inf in enumerate(tmp_list):
                tmp = inf.split('\n')
                for i in tmp:
                    tm = [j for j in i.split(' ') if j != '']
                    tmp_2_list[num].extend(tm)
                
        self.last_info = self.info
        if len(last_info_list) != len(info_list):
            self.diff_info = self.info.split('\n')
        else:
            for num, i in enumerate(info_list):
                if last_info_list[num] != i:
                    self.diff_info.append(i)
               
    def light_font(self):
        flash_font = QTextCharFormat()
        flash_font.setForeground(Qt.black)
        flash_font.setFontWeight(QFont.Normal)
        flash_font.setBackground(Qt.lightGray)
        flash_font.setFont(QFont('Arial', 11))
        self.replace_text(flash_font)
        
        
    def normal_font(self):
        self.replace_text()
        
    def replace_text(self, flash_font = None):
        self.current = self.show_info.toPlainText()
        for i in self.diff_info:
            start_of_word = self.current.find(i.strip())
            self._cursor.setPosition(start_of_word)
            self._cursor.setPosition(start_of_word + len(i.strip()), QTextCursor.KeepAnchor) #選取需要置換的區域
            if flash_font:
                self._cursor.insertText(i.strip(), flash_font)
            else:
                self._cursor.insertText(i.strip(), self.inner_font)

    
    def hightlight_selection(self, event):
        light_font = QTextCharFormat()
        light_font.setForeground(Qt.black)
        light_font.setFontWeight(QFont.Normal)
        light_font.setBackground(Qt.yellow)

        if self.last_cursor:
            self._cursor.setPosition(self.last_cursor)
            self._cursor.movePosition(QTextCursor.StartOfLine)
            self._cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            self._cursor.insertText(self._cursor.selectedText(), self.inner_font)
            self._cursor.removeSelectedText()
            self.last_cursor = None

        cursor = self.show_info.cursorForPosition(event.pos())
        position = cursor.position() 
        self._cursor.setPosition(position)
        self._cursor.movePosition(QTextCursor.StartOfLine)
        self._cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        if self._cursor.hasSelection() and self._cursor.selectedText().strip() in schedule_set:
            tmp_info = self._cursor.selectedText().strip()
            self.last_cursor = position
            self._cursor.insertText(self.inner_space, self.inner_font)
            self._cursor.movePosition(QTextCursor.EndOfLine)
            self._cursor.insertText(tmp_info, light_font)
    
    def open_delete_key(self, event):
        if event.key() == Qt.Key_Delete and self.last_cursor:
            self.del_schedular_set()


    def del_schedular_set(self):
        if self.last_cursor:
            self._cursor.setPosition(self.last_cursor)
            self._cursor.movePosition(QTextCursor.StartOfLine)
            self._cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            if self._cursor.hasSelection():    
                schedule_set.remove(self._cursor.selectedText().strip())                   
                self._cursor.removeSelectedText()
                self._cursor.deletePreviousChar()
                #寫回排程紀錄裡
                self.last_cursor = None
    
    def change_mouse_shape(self, event):
        now_cursor = self.show_info.cursorForPosition(event.pos())
        now_position = now_cursor.position() 
        self.current = self.show_info.toPlainText()
        area_start = self.current.find(schedule_set[0])
        area_end = self.current.find(schedule_set[-1]) + len(schedule_set[-1])
        if now_position in range(area_start, area_end):
            self.show_info.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.show_info.viewport().setCursor(Qt.CursorShape.IBeamCursor)

    #region 得到使用者即時選擇的資訊並且傳回給顯示面板
    def get_real_info(self, text):
        self.get_now_time()   #更新最新時間
        information_index = 0
        info = ''
        if text in project:       #使用者選擇project時
            information_index = self.information.index('Select Project:')
            info = text
        #settime = ['Current shift', 'Today', 'This Week', 'A Week' ,'1 day shift', '1 night shift']
        if text in time_selection and text != 'Select time':
            information_index = self.information.index('Set Time:')
            #Current shift 今日早上8點到現在時間
            if text == time_selection[0]:                     
                info = self.nowdate + ' 08:00' + ' ~' + '\n' + self.inner_space + self.nowdatetime
            #Today 今日0點到現在時間
            if text == time_selection[1]:                      
                info = self.nowdate + ' 00:00' + ' ~' + '\n' + self.inner_space + self.nowdatetime
            #This Week 這禮拜一 0點 到 現在時間點
            if text == time_selection[2]:                      
                delta = timedelta(days = datetime.today().weekday())
                thisweek = self.now - delta
                thisweek_date = thisweek.strftime('%Y/%m/%d')
                info = thisweek_date + ' 00:00' + ' ~' + '\n' + self.inner_space + self.nowdatetime
            #A Week 一個禮拜
            if text == time_selection[3]:                      
                lastweek = self.now - timedelta(weeks = 1)
                lastweek_datetime = lastweek.strftime('%Y/%m/%d')
                info = lastweek_datetime + ' 00:00' + ' ~' + '\n' + self.inner_space + self.nowdatetime
            #1 day shift  昨天8點 到 現在時間點
            if text == time_selection[4]:                    
                delta = timedelta(days = 1)
                yesterday = self.now - delta
                yesterday_date = yesterday.strftime('%Y/%m/%d')
                info = yesterday_date + ' 08:00' + ' ~' + '\n' + self.inner_space + self.nowdate + ' 20:00' 
            #1 night shift 過一晚上，昨天下班(晚上8點) 到 現在時間點
            if text == time_selection[5]:  
                delta = timedelta(days = 1)
                yesterday = self.now - delta
                yesterday_date = yesterday.strftime('%Y/%m/%d')                   
                info = yesterday_date + ' 20:00' + ' ~' + '\n' + self.inner_space + self.nowdate + ' 08:00'
        
        #如果text為使用這自己選擇的日期時間(當text為'Select time' 或是 他的type為數字(選擇時間) 或是 他的type為QtCore.QDate(使用日曆選擇時間))
        if  text == 'Select time' or text == 'selecttime_change':     
            information_index = self.information.index('Set Time:')
            info = self.date_start.date().toString('yyyy/MM/dd') + ' ' + self.day_start_time.currentText() + ' ~' + '\n' + self.inner_space + self.date_end.date().toString('yyyy/MM/dd')+ ' ' +  self.day_end_time.currentText()
       
        #如果text為使用者改變排程日期時
        if  type(text) == QtCore.QTime:       
            information_index = self.information.index('Set Task Scheduler Time:')
            temp = self.schedular_time.time().toString()
            info = temp.split(':')[0] + ':' + temp.split(':')[1]
    
        return information_index, info  
        #endregion 


    #設定執行狀態顯示字體
    def set_show_current_status(self):
        self.show_status = self._window.plainTextEdit_2
        self.status_cursor = self.show_status.textCursor()
        self.show_status.setReadOnly(True)
        self.show_status.setStyleSheet("background : black")
        #self.show_current.setFocus()
        self.exefont = self.show_status.currentCharFormat()
        self.exefont.setForeground(Qt.green)
        self.exefont.setFontWeight(QFont.Normal)
        self.exefont.setFontPointSize(10)
        self.show_status.moveCursor(QTextCursor.End)
        self.show_status.setCurrentCharFormat(self.exefont)
    
    #顯示下方狀態字幕
    def show_current_status(self, text):
        self.get_now_time()
        status_space = ' '*2
        self.show_status.appendPlainText(self.now_H_M + status_space + text)

    
    #錯誤視窗
    def errobox(self, text):
        QMessageBox.warning(self, 'error', text, QMessageBox.Ok)

    #檢查時間並且執行        
    def check_datetime(self):
        if self.time_selection.currentText() == 'Select time':
            start_time = self.date_start.date().toString(Qt.ISODate) + ' ' + self.day_start_time.currentText() + ':00'
            end_time = self.date_end.date().toString(Qt.ISODate)+ ' ' + self.day_end_time.currentText() + ':00'
            start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            
            if start > self.now or end > self.now:
                self.execute_flag = False
                self.errobox('不能超過現在時間!')
                     
            elif end < start:
                self.execute_flag = False
                
                self.errobox('結束時間不能在起始時間之前!')
                    
            elif abs(end-start).days >= 30:
                self.execute_flag = False
                self.errobox('時間間格不能大於一個月!')
                
    def get_execute_data(self):
        information_index, time_period = self.get_real_info(self.time_selection.currentText())
        self.execute_data = {
        'site':'蘇州',
        'data_source':'Test Station',
        'user_select_project': self.pro_selection.currentText(),
        'time_selection':{'time': self.time_selection.currentText(), 'time_period':[time_period.split('~')[0].strip(), time_period.split('\n')[1].strip()],
        'Download_path':self.download_path.text()}
        }
        print(self.execute_data)

    #執行按鈕
    def Execute_btm(self):
        self.execute = self._window.pushButton
        self.execute.clicked.connect(self.execute_flow)
    
    def Stop_btm(self):
        self.stop = self._window.pushButton_3
    
    def Exit_btm(self):
        self.Exit = self._window.pushButton_2
        self.Exit.clicked.connect(self.exit)
    
    def execute_flow(self):
        self.check_datetime()
        if self.execute_flag:
            self.execute_disable()
            self.start_thread()
            self.get_execute_data()
         
    def start_thread(self):
        self.start = start_prcess(self.execute_data)
        self.start.signal.status.connect(self.show_current_status)
        self.start.signal.error.connect(self.errobox)
        self.threadpool.start(self.start)


    def exit(self):
        self.close()


class thread_signal(QObject):
    status = Signal(str)
    error = Signal(str)

class start_prcess(QRunnable):
    def __init__(self, execute_data):
        super(start_prcess, self).__init__()  
        self.signal = thread_signal()
        self.execute_data = execute_data
    
    def run(self):
        self.tt = tests.test_2.test_flow(self.execute_data, self.signal)


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