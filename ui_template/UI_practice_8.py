import sys
import PySide6.QtGui
from PySide6.QtWidgets import (QPushButton, QWidget, QLineEdit,
                               QApplication)

class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent) 
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        self.setText(event.mimeData().text())

class Drag(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 65)

        button = Button("Button", self)
        button.move(190, 65)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Simple Drag')
        

def main():
    app = QApplication(sys.argv)
    ex=Drag()
    ex.show()
    app.exec()

if __name__ == '__main__':
    main()