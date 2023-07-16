import sys
from PySide6.QtWidgets import (QWidget, QToolTip,
                               QPushButton, QApplication, QMessageBox)
from PySide6.QtGui import QFont

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.center()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50,50)

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Tooltips')
        self.show()

    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.StandardButton.Yes 
                            |QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
    
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    




def main():
    app = QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()