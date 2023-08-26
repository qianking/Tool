from PySide6.QtWidgets import (QWidget, QCheckBox, QPushButton,
                               QFrame, QApplication, QSlider,
                               QLabel, QProgressBar, QCalendarWidget,
                               QVBoxLayout)
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Qt, QBasicTimer, QDate
import sys

class CheckBox(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        check = QCheckBox('Title Set', self)
        check.setCheckState(Qt.CheckState.Checked)

        check.move(20,20)
        check.stateChanged.connect(self.changetitle)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('QCheckBox')
        self.show()

    def changetitle(self, state):
        if state == Qt.CheckState.Checked:
            self.setWindowTitle('Qcheckbox')
        else:
            self.setWindowTitle(' ')

class ToggleBtn(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.col = QColor(0,0,0)
        redb = QPushButton('red', self)
        redb.setCheckable(True)
        redb.move(10, 10)

        redb.clicked[bool].connect(self.setcolor)

        greenb = QPushButton('green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setcolor)

        blueb = QPushButton('blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setcolor)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color:%s }"% self.col.name())
        self.frm.setGeometry(130, 22, 200, 200)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('QCheckBox')
        self.show()

    def setcolor(self, pressed):

        source = self.sender()

        if pressed:
            val = 255
        else:
            val = 0

        if source.text() == 'red':
            self.col.setRed(val)
        elif source.text() == 'green':
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)

        self.frm.setStyleSheet("QWidget { background-color:%s }"% self.col.name())


class Slider(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        sld = QSlider(Qt.Orientation.Horizontal, self)
        sld.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        sld.setGeometry(30, 40, 200, 30)
        sld.valueChanged[int].connect(self.changeValue)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('mute.png'))
        self.label.setGeometry(250, 40, 80, 30)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('QSlider')
        self.show()
    
    def changeValue(self, value):
        if value == 0:
            pass
        elif 0< value <= 30:
            pass


class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40 ,200, 25)

        self.btn = QPushButton('start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('QProgressBar')
        self.show()
    
    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step +1
        self.pbar.setValue(self.step)
    
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')

class Calendar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QDate].connect(self.showDate)

        vbox.addWidget(cal)

        self.lbl = QLabel(self)
        #date = cal.selectedDate()
        #self.lbl.setText(date.toString())

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('QCalendar')
        self.show()
    
    def showDate(self, date):
        self.lbl.setText(date.toString())


def main():
    app = QApplication(sys.argv)
    ex=Calendar()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()