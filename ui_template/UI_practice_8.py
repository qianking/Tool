import sys
from PySide6.QtGui import QDrag
from PySide6.QtCore import Qt, QMimeData
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



class Button2(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
    
    def mouseMoveEvent(self, Event):
        if Event.buttons() != Qt.MouseButton.RightButton:
            return 
        
        mimeDate = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeDate)

        drag.setHotSpot(Event.position().toPoint() - self.rect().topLeft())
        dropAction = drag.exec(Qt.DropAction.MoveAction)
    
    def mousePressEvent(self, Event):
        super().mousePressEvent(Event)

        if Event.buttons() == Qt.MouseButton.LeftButton:
            print('press')

class Move(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.button = Button2('Button', self)
        self.button.move(100, 65)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('click and move')

    def dragEnterEvent(self, event):
        event.accept()
    
    def dropEvent(self, event):
        position = event.position()
        self.button.move(position.toPoint())

        event.setDropAction(Qt.DropAction.MoveAction)
        event.accept()
        

def main():
    app = QApplication(sys.argv)
    ex=Move()
    ex.show()
    app.exec()

if __name__ == '__main__':
    main()