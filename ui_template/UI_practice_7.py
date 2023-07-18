import sys
from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QApplication)

class LineEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        