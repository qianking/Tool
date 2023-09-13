import sys
from PySide6.QtGui import QDrag, QPixmap
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtWidgets import (QPushButton, QWidget, QLineEdit,
                               QApplication, QHBoxLayout)


class DragButton(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
    
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            mime = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mime)

            #self.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0.5); color: white;}')
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.exec(Qt.MoveAction)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setAcceptDrops(True)

    def initUI(self):
        self.blayout = QHBoxLayout(self)

        for L in ['A', 'B', 'C', 'D', 'E']:
            btn = DragButton(L, self)
            self.blayout.addWidget(btn)

        self.setLayout(self.blayout)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Drag and Move')
    
    def dragEnterEvent(self, event):
        event.accept()
    
    def dropEvent(self, event):
        position = event.position()
        widget = event.source()

        for n in range(self.blayout.count()):
            w = self.blayout.itemAt(n).widget()
            if position.x() < w.x() + w.size().width()//2:
                self.blayout.insertWidget(n-1, widget)
                break
        
        event.accept()









def main():
    app = QApplication(sys.argv)
    ex=Window()
    ex.show()
    app.exec()

if __name__ == '__main__':
    main()