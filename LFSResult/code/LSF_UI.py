from glob import glob
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QRadioButton, QLabel, QLineEdit, QHBoxLayout, QPlainTextEdit, QFileDialog, QTextBrowser,QMessageBox
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtCore import Qt, Signal, QRunnable, QObject, QThreadPool, QTimer, QUrl
from LSF_Main import Main

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data = dict()
        self.start_flag = True
        self.dot_count = 0
        self.timer = QTimer()
        self.threadpool = QThreadPool()
        self.initialize()
        self.showResultSet()
        self.optionBtmSet()
        self.import_btm_connect()
        self.start_btm_connect()
    
    def initialize(self):
        self.setWindowTitle("LSFResult")

        self.generallayout = QVBoxLayout()
        self.option_btm = QRadioButton("校正")

        self.input_layout = QHBoxLayout()
        self.label_level = QLabel("Level: ")
        self.label_H = QLabel("H(m): ")
        self.level_input = QLineEdit()
        self.H_input = QLineEdit()

        self.label_level.setEnabled(False)
        self.label_H.setEnabled(False)
        self.level_input.setEnabled(False)
        self.H_input.setEnabled(False)

        self.input_layout.addWidget(self.label_level)
        self.input_layout.addWidget(self.level_input)
        self.input_layout.addWidget(self.label_H)
        self.input_layout.addWidget(self.H_input)

        self.import_btm = QPushButton("Import")
        self.start_btm = QPushButton("Start")
        self.start_btm.setEnabled(False)
        self.btmlayout = QHBoxLayout()
        self.btmlayout.addWidget(self.import_btm)
        self.btmlayout.addWidget(self.start_btm)
        
        self.show_result = QTextBrowser()

        self.generallayout.addLayout(self.btmlayout)
        self.generallayout.addWidget(self.option_btm)
        self.generallayout.addLayout(self.input_layout)
        self.generallayout.addWidget(self.show_result)

        self.setLayout(self.generallayout)

    #region 結果顯示設定
    def showResultSet(self):
        self.show_result.setLineWrapMode(QTextBrowser.NoWrap)
        self.show_result.setReadOnly(True)

    def setDisplayText(self, show_data:tuple):
        txt, color = show_data
        fft1 = self.show_result.currentCharFormat()
        fft1.setForeground(color)     
        self.show_result.setCurrentCharFormat(fft1)
        self.show_result.insertPlainText(f"{txt}\n")
    #endregion

    #region 校正選擇紐設定
    def optionBtmSet(self):
        self.option_btm.toggled.connect(self.hidden)
    
    def hidden(self, checked):
        if checked:
            self.label_level.setEnabled(True)
            self.label_H.setEnabled(True)
            self.level_input.setEnabled(True)
            self.H_input.setEnabled(True)
        else:
            self.label_level.setEnabled(False)
            self.label_H.setEnabled(False)
            self.level_input.setEnabled(False)
            self.H_input.setEnabled(False)
    #endregion
    
    #region 選擇資料夾設定
    def import_btm_connect(self):
        self.import_btm.clicked.connect(self.select_folder)

    def select_folder(self):
        self.show_result.clear()
        input_folder_path = QFileDialog.getExistingDirectory(self, 'choose folder', 'F:/Job')
        input_folder_path = input_folder_path.replace("/", "\\")
        self.setDisplayText((f"選擇路徑: {input_folder_path}", Qt.black))
        self.file_Check(input_folder_path)

    def file_Check(self, input_folder_path):
        compare_dic={'VPDATXE.txt':'input_X',
                     'VPDATXE_NSW.txt':'input_X_shear', 
                     'VPDATYE.txt':'input_Y',
                     'VPDATYE_NSW.txt':'input_Y_shear'}
        
        self.data['input_path'] = input_folder_path
        file_list = glob(f"{input_folder_path}\*.txt")

        self.setDisplayText((f"內容: ", Qt.black))
        for file in file_list:
            file_t = file.split('\\')[-1]
            self.setDisplayText((f"  {file_t}", Qt.black))

            for key, value in compare_dic.items():
                if file.endswith(key):
                    self.data[value] = file
        
        if len(file_list) == 4:
            self.setDisplayText((f"總共發現{len(file_list)}個檔案, 檔案正確\n", Qt.darkYellow))
            self.start_btm.setEnabled(True)
        else:
            self.setDisplayText((f"發現{len(file_list)}個檔案, 有檔案缺少!!", Qt.red))
            self.Reset_To_Defult()
    #endregion

    #region 獲得校正狀態與資料
    def get_correction_data(self):
        ifcorrection = self.option_btm.isChecked()
        self.data['adjust'] = ifcorrection
        if ifcorrection:
            self.data['level'] = self.level_input.text().strip()
            self.data['H'] = self.H_input.text().strip()
            try:
                self.data['H'] = float(self.data['H'])
            except:
                self.setDisplayText((f"H(m)請填入數字!!", Qt.red))
                self.start_flag = False
        
            if self.data['level'] == '':
                self.setDisplayText((f"Level請填入值!!", Qt.red))
                self.start_flag = False  
    #endregion

    #region 開始按鈕設定
    def start_btm_connect(self):
        self.start_btm.clicked.connect(self.get_correction_data) 
        self.start_btm.clicked.connect(self.start_flow)
    #endregion

    def start_flow(self):
        if self.start_flag:
            self.startuiset()
            self.start_animate()
            self.start_thread()

    def startuiset(self):
        self.start_btm.setEnabled(False)
        self.import_btm.setEnabled(False)

    #region 字串動畫設定
    def start_animate(self):
        self.timer.timeout.connect(lambda:self.string_animate('轉換中'))  
        self.timer.setInterval(500)
        self.timer.start()

    def string_animate(self, txt):
        fmt = self.show_result.currentCharFormat()
        fmt.setForeground(QColor("red"))  

        cursor = self.show_result.textCursor()  
        cursor.movePosition(cursor.End)
        cursor.movePosition(cursor.StartOfLine, cursor.KeepAnchor)
        lastLine = cursor.selectedText()

        if txt in lastLine:
            cursor.removeSelectedText()

        cursor.insertText(txt + '.' * self.dot_count, fmt)
        self.dot_count = (self.dot_count + 1) % 4  # 讓'.'在0到3之間循環
    #endregion

    #region 警告視窗
    def MSGBox_WARN(self, txt):
        self.Reset_To_Defult()
        QMessageBox.warning(self, "Oops", txt)
        self.setDisplayText((f"已停止", Qt.red)) 
    #endregion

    #region reset to defult
    def Reset_To_Defult(self):
        self.data.clear()
        self.start_flag = True
        self.dot_count = 0
        self.timer.stop()
        self.start_btm.setEnabled(False)
        self.import_btm.setEnabled(True)
    #endregion

    def finish(self):
        self.setDisplayText(("\nDone!", Qt.black))
        self.Reset_To_Defult()
        self.timer.stop()

    #region 超連結
    def show_outputpath(self, path:str):
        self.show_result.setOpenLinks(False)
        self.show_result.setOpenExternalLinks(False)
        self.show_result.append(f"<a href='file:///{path}'>Open File</a>")
        self.show_result.anchorClicked.connect(self.open_file)

    def open_file(self, url):
        QDesktopServices.openUrl(url)
    #endregion

    #region transfer thread
    def start_thread(self):
        print(self.data)
        self.start_thread = start_process(self.data)
        self.start_thread.signals.status.connect(self.setDisplayText)
        self.start_thread.signals.exception.connect(self.MSGBox_WARN)
        self.start_thread.signals.finish.connect(self.finish)
        self.start_thread.signals.final_path.connect(self.show_outputpath)
        self.threadpool.start(self.start_thread)
    #endregion


class ThreadSignal(QObject):
    status = Signal(tuple)
    exception = Signal(str)
    finish = Signal()
    final_path = Signal(str)

class start_process(QRunnable):
    def __init__(self, data):
        super(start_process, self).__init__()  
        self.signals = ThreadSignal()
        self.data = data
        
    def run(self):
        Main(self.data, self.signals)    

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec()