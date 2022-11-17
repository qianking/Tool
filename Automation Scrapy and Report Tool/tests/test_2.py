from re import M
import sys
import os
#import threading
import time
import threading
import ctypes
import time
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget, QMainWindow, QLabel,  QHBoxLayout, QGridLayout
#from threading import Thread



def choose_chrome_path():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    centralwidget = QWidget(MainWindow)
    label = QLabel(centralwidget)
    font = QFont("Arial", 12)
    label.setFont(font)

    label.setAlignment(Qt.AlignCenter)
    g_layout = QGridLayout(centralwidget)
    g_layout.addWidget(label, 0, 0, 0, 0)
    MainWindow.setCentralWidget(centralwidget)
    MainWindow.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)


    filename_choose, filetype = QFileDialog.getOpenFileName(MainWindow, 'Choose chrome path', 'C:/', "exe File (*exe)")
    if filename_choose.split('/')[-1] != "chrome.exe":
        wrong_chrome_path_box()
        choose_chrome_path()
    else:
        label.setText(f"選擇路徑:\n{filename_choose}\n (三秒後關閉)")
        QTimer.singleShot(3000, MainWindow.close)
        return filename_choose.replace("/", "\\")
    MainWindow.show()
    app.exec()


class another(QWidget):
    def __init__(self):
        super(another, self).__init__()
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle('Warning')
        MessageBox.setText("這台電腦的google chrome路徑不為預設路徑，請選擇正確的chrome.exe路徑，以完成後續的設定")
        font = QFont("Arial", 12)
        MessageBox.setFont(font)



    
def wrong_chrome_path_box():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    MessageBox = QMessageBox()
    MessageBox.setWindowTitle('Warning')
    MessageBox.setText("請選擇正確的chrome.exe檔案")
    font = QFont("Arial", 12)
    MessageBox.setFont(font)
    MessageBox.show()
    app.exec()


#last_check_time = None
''' driver_mapping = dict()
driver_mapping.items()
lll = driver_mapping.get('chrome_major_ver')
print(lll)
 '''





    

    



    


