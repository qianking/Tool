from glob import glob
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QRadioButton, QLabel, QLineEdit, QHBoxLayout, QPlainTextEdit, QFileDialog
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data = dict()
        self.initialize()
        self.showResultSet()
        self.optionBtmSet()
        self.import_btm_connect()
    
    def initialize(self):
        self.setWindowTitle("LSF")

        self.generallayout = QVBoxLayout()
        self.option_btm = QRadioButton("校正")

        self.input_layout = QHBoxLayout()
        self.label_level = QLabel("Level: ")
        self.label_H = QLabel("H(m)")
        self.level_input = QLineEdit()
        self.H_input = QLineEdit()

        self.label_level.setEnabled(False)
        self.label_H.setEnabled(False)
        self.level_input.setEnabled(False)
        self.H_input.setEnabled(False)

        self.input_layout.addWidget(self.label_level)
        self.input_layout.addWidget(self.level_input)
        self.input_layout.addWidget(self.label_H)
        self.input_layout.addWidget(self.H_input)

        self.import_btm = QPushButton("Import")
        self.start_btm = QPushButton("Start")
        self.btmlayout = QHBoxLayout()
        self.btmlayout.addWidget(self.import_btm)
        self.btmlayout.addWidget(self.start_btm)

        self.show_result = QPlainTextEdit()

        self.generallayout.addLayout(self.btmlayout)
        self.generallayout.addWidget(self.option_btm)
        self.generallayout.addLayout(self.input_layout)
        self.generallayout.addWidget(self.show_result)

        self.setLayout(self.generallayout)

    def showResultSet(self):
        self.show_result.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.show_result.setReadOnly(True)


    def setDisplayText(self, show_data:tuple):
        txt, color = show_data
        fft1 = self.show_result.currentCharFormat()
        fft1.setForeground(color)     
        self.show_result.setCurrentCharFormat(fft1)
        self.show_result.insertPlainText(f"{txt}\n")

    def optionBtmSet(self):
        self.option_btm.toggled.connect(self.hidden)
    
    def hidden(self, checked):
        if checked:
            self.label_level.setEnabled(True)
            self.label_H.setEnabled(True)
            self.level_input.setEnabled(True)
            self.H_input.setEnabled(True)
        else:
            self.label_level.setEnabled(False)
            self.label_H.setEnabled(False)
            self.level_input.setEnabled(False)
            self.H_input.setEnabled(False)
    
    def import_btm_connect(self):
        self.import_btm.clicked.connect(self.select_folder)

    def select_folder(self):
        self.show_result.clear()
        input_folder_path = QFileDialog.getExistingDirectory(self, 'choose folder', 'F:/Job')
        input_folder_path = input_folder_path.replace("/", "\\")
        self.setDisplayText((f"選擇路徑: {input_folder_path}", Qt.black))
        file_list = glob(f"{input_folder_path}\*.txt")

        self.data['input_path'] = input_folder_path
        self.data['file_list'] = file_list
        self.data['file_name_dic'] = {file.split('\\')[-1].split('.')[0]: file for file in file_list}
        for file in file_list:
            file = file.split('\\')[-1]
            self.setDisplayText((f"   {file}", Qt.black))
        self.setDisplayText((f"總共發現{len(file_list)}個檔案", Qt.darkYellow))
    
    

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec()