#file:///c:/users/andy_chien/Downloads/EZ1KA2ACT2-8.txt


from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget,QTextBrowser

""" class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        layout = QVBoxLayout()

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenLinks(True)
        self.text_browser.setOpenExternalLinks(True)
        path = 'E:/python/virtualenv/Tool/Tool data/'
        self.text_browser.setHtml(f"<a href='{path}'>Open File</a>")
        
        self.text_browser.anchorClicked.connect(self.open_file)

        layout.addWidget(self.text_browser)
        self.setLayout(layout)

    def open_file(self, url):
        QDesktopServices.openUrl(QUrl.fromLocalFile(url))  """


class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        layout = QVBoxLayout()

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenLinks(False)
        self.text_browser.setOpenExternalLinks(False)
        path = r'E:\python\virtualenv\Tool\Tool data\LSFResult\data\資料\弱層檢核\V534\VPDATXE.txt'
        self.text_browser.setHtml(f"<a href='file:///{path}'>Open File</a>")

        self.text_browser.anchorClicked.connect(self.open_file)

        layout.addWidget(self.text_browser)
        self.setLayout(layout)

    def open_file(self, url):
        #QDesktopServices.openUrl(QUrl.fromLocalFile(url))
        QDesktopServices.openUrl(url)
if __name__ == "__main__":
    app = QApplication([])
    widget = SimpleGUI()
    widget.show()
    app.exec()



