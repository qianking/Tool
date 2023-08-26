from PySide6.QtWidgets import (QWidget, QPushButton, QLineEdit, 
                               QInputDialog, QApplication, QFrame,
                               QColorDialog, QFileDialog, QTextEdit, 
                               QMainWindow)

from PySide6.QtGui import QColor, QAction, QIcon
from pathlib import Path
import sys

class Dialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 300, 300)

        self.setWindowTitle('Input Dialog')
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        if ok:
            self.le.setText(str(text))

class Color(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        col = QColor(0, 0, 0)
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color:%s }"% col.name())
        self.frm.setGeometry(130, 22, 200, 200)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('color dialog')
        self.show()
    
    def showDialog(self):

        col = QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color:%s }"% col.name())

class File(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.txt = QTextEdit(self)
        self.setCentralWidget(self.txt)
        self.statusBar()

        openfile = QAction(QIcon('open.png'), 'Open', self)
        openfile.setShortcut('Ctrl+0')
        openfile.setStatusTip('Open new File')
        openfile.triggered.connect(self.showDialog)

        menu = self.menuBar()
        filemenu = menu.addMenu('&File')
        filemenu.addAction(openfile)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('file dialog')
        self.show()

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.txt.setText(data)


   
def main():
    app = QApplication(sys.argv)
    ex=File()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
     

