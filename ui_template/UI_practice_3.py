import sys
from PySide6.QtWidgets import (QMainWindow, QApplication, 
                               QLineEdit, QTextEdit, QPushButton,
                               QGridLayout, QWidget, QLabel)


class Calaulator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):

            if name == '':
                continue

            btn = QPushButton(name)
            grid.addWidget(btn, *position)

        
        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()


class Review(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)


        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()






def main():
    app = QApplication(sys.argv)
    ex=Review()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()