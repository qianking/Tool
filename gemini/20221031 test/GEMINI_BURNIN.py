import sys
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore
from Burnin_ui_controller import MainWindow


if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.show()       

    sys.exit(app.exec())
   