import sys
import PySide6.QtGui
from PySide6.QtWidgets import (QWidget, QLCDNumber, QSlider, 
                               QVBoxLayout, QApplication, QGridLayout, 
                               QLabel, QMainWindow, QPushButton)
from PySide6.QtCore import Qt



class Signal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lcd = QLCDNumber(self)
        slider = QSlider(Qt.Orientation.Horizontal, self)

        slider.valueChanged.connect(lcd.display)

        vlayout = QVBoxLayout()
        vlayout.addWidget(lcd)
        vlayout.addWidget(slider)

        self.setLayout(vlayout)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Signal')
        self.show()


class MouseMove(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        x= 0
        y= 0
        self.label = QLabel(f"x: {x}, y: {y}", self)
        grid = QGridLayout()

        grid.addWidget(self.label, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.setMouseTracking(True)
        self.setLayout(grid)
       
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Event object')
        self.show()

    def mouseMoveEvent(self, event):

        x = int(event.position().x())
        y = int(event.position().y())

        text = f"x: {x}, y: {y}"
        self.label.setText(text)


class Sender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        btn_1 = QPushButton('Button 1', self)
        btn_1.move(50, 150)

        btn_2 = QPushButton('Button 2', self)
        btn_2.move(150, 150)

        self.statusBar()

        btn_1.clicked.connect(self.buttonCliecked)
        btn_2.clicked.connect(self.buttonCliecked)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Event sender')
        self.show()


    def buttonCliecked(self):
        
        sender = self.sender()
        msg = f"{sender.text()} was pressed"
        self.statusBar().showMessage(msg)


def main():
    app = QApplication(sys.argv)
    ex=Sender()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

