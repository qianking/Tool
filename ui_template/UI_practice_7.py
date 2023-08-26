import sys
from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QApplication,
                               QSplitter, QHBoxLayout, QFrame)
from PySide6.QtCore import Qt

class LineEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        qle = QLineEdit(self)
        qle.move(60, 100)
        self.lbl.move(60, 40)

        qle.textChanged[str].connect(self.onChanged)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('QLinedit')
        self.show()

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


class Spliter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout(self)

        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.Shape.StyledPanel)

        topright = QFrame(self)
        topright.setFrameShape(QFrame.Shape.StyledPanel)

        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.Shape.StyledPanel)

        spliter1 = QSplitter(Qt.Orientation.Horizontal)
        spliter1.addWidget(topleft)
        spliter1.addWidget(topright)

        spliter2 = QSplitter(Qt.Orientation.Vertical)
        spliter2.addWidget(spliter1)
        spliter2.addWidget(bottom)

        hbox.addWidget(spliter2)
        self.setLayout(hbox)

        self.setGeometry(300, 300, 450, 400)
        self.setWindowTitle('QSplitter')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex=Spliter()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()