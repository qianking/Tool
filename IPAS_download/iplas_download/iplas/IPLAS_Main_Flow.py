import sys
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtWidgets
from Pre_proccess_controller import Pre_process 
import Pre_proccess 




if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()
w = Pre_process()
w.show()
app.exec()

    









