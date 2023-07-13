#file:///c:/users/andy_chien/Downloads/EZ1KA2ACT2-8.txt


from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget,QTextBrowser

class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        layout = QVBoxLayout()

        self.text_browser = QTextBrowser()
        file_path = QUrl.fromLocalFile("c:/users/andy_chien/Downloads/EZ1KA2ACT2-8.txt")
        self.text_browser.setHtml(f"<a href='{file_path.toString()}'>Open File</a>")
        self.text_browser.setOpenExternalLinks(False)
        self.text_browser.anchorClicked.connect(self.open_file)

        layout.addWidget(self.text_browser)
        self.setLayout(layout)

    def open_file(self, url):
        QDesktopServices.openUrl(url)

    def initialize_ui(self):
        layout = QVBoxLayout()

        self.text_browser = QTextBrowser()
        self.text_browser.setHtml("<a href='c:/users/andy_chien/Downloads/'>Open File</a>")
        self.text_browser.setOpenLinks(True)
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.anchorClicked.connect(self.open_file)

        layout.addWidget(self.text_browser)
        self.setLayout(layout)

    def open_file(self, url):
        QDesktopServices.openUrl(QUrl.fromLocalFile(url)) 

if __name__ == "__main__":
    app = QApplication([])
    widget = SimpleGUI()
    widget.show()
    app.exec()



