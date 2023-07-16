import sys
from PySide6.QtWidgets import (QMainWindow, QApplication, QMenu, QTextEdit)
from PySide6.QtGui import QIcon, QAction

class MenuBar(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File') #有&表示可以按Alt來顯示快捷鍵，並且按下Alt+快捷鍵來打開該選單
        self.statusbar = self.statusBar()  #顯示setStatusTip的字
        self.statusbar.showMessage('Ready')

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)

        impMenu = QMenu('&Import', self)
        impact = QAction('Import mail', self)
        impMenu.addAction(impact)

        newact = QAction('&New', self)

        viewStatAct = QAction('View Statusbar', self, checkable=True)
        viewStatAct.setStatusTip('View Statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)



        fileMenu.addAction(newact)
        fileMenu.addMenu(impMenu)
        fileMenu.addAction(exitAct)
        fileMenu.addAction(viewStatAct)


        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('menu')
        self.show()
    
    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        newAct = cmenu.addAction('New')
        openAct = cmenu.addAction('Open')
        quitAct = cmenu.addAction('Quit')
        action = cmenu.exec(self.mapToGlobal(event.pos()))

        if action == quitAct:
            QApplication.instance().quit()
    
    def toggleMenu(self, status):
        if status:
            self.statusbar.show()
        else:
            self.statusbar.hide()


class Toolbar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex=Toolbar()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
