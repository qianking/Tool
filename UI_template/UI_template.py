import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtCore import QFile, QTimer, QDate, QTime, QThread, Signal, QObject, QPoint, QCoreApplication, Qt
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QFileDialog, QPlainTextEdit, QWidget, QDialog
from PySide6.QtGui import QColor, QPalette, QFont

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QLabel, QPushButton, QLineEdit
from PySide2.QtGui import QFont, QIcon


class MainWindow(object):
    def __init__(self, parent=None):
        self._window = None
        self.setup_ui()

    @property
    def window(self):
        return self._window

    def setup_ui(self):
        loader = QUiLoader()
        file = QFile('./')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()





if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    qt_app = QtWidgets.QApplication(sys.argv)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.window.show()

    sys.exit(app.exec())