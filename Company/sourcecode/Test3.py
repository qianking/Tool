""" import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from qtrangeslider import QRangeSlider

class RangeSliderDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 創建一個QRangeSlider
        self.range_slider = QRangeSlider(Qt.Orientation.Horizontal, self)
        self.range_slider.setRange(0, 200)
        self.range_slider.setValue([10,50])
        self.range_slider.valueChanged[tuple].connect(self.update_label)
        print(self.range_slider.value())

        # 創建一個QLabel來顯示選擇的範圍
        #self.update_label()

        layout.addWidget(self.range_slider)

        self.setLayout(layout)
        self.setWindowTitle('QRangeSlider Demo')
        self.show()
    
    def update_label(self, value):
        
        print(value[0], value[1])

app = QApplication(sys.argv)
demo = RangeSliderDemo()
sys.exit(app.exec_()) """

# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
# from PySide6.QtCore import Qt

# class CustomSlider(QWidget):
#     def __init__(self):
#         super(CustomSlider, self).__init__()

#         self.setFixedSize(400, 150)  # Set fixed window size

#         layout = QVBoxLayout()

#         self.slider = QSlider(Qt.Horizontal)
#         self.slider.setMinimum(0)
#         self.slider.setMaximum(360)
#         self.slider.setFixedWidth(380)
#         self.slider.setFixedHeight(50)
#         self.slider.setSingleStep(30)
#         self.slider.setTickPosition(QSlider.TicksBelow)
#         self.slider.setTickInterval(60)

#         layout.addWidget(self.slider)

#         # Create labels for specific angles
#         angles = [0, 60, 120, 180, 240, 300, 360]
#         self.create_labels(angles)

#         self.setLayout(layout)
#         self.setWindowTitle("HSV Color Slider")
#         self.show()

#     def create_labels(self, angles):
#         slider_width = self.slider.width() - 22  # Estimate the boundary width
        

#         for angle in angles:
#             label = QLabel(str(angle), self)
#             label.setFixedWidth(50)  # Set width
#             position_percentage = angle / 360
#             print(label.width())
#             position_pixel = (slider_width * position_percentage) - (label.width() / 2)
#             print(position_pixel)
#             label.move(position_pixel+38, self.slider.height() + 35)  # Move label to the desired position under the slider

# app = QApplication(sys.argv)
# window = CustomSlider()
# sys.exit(app.exec_())

import sys
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 創建按鈕並設置信號連接
        self.button = QPushButton("Open Table", self)
        self.button.clicked.connect(self.open_table_window)

        self.setCentralWidget(self.button)
        self.setWindowTitle("Open Table Window")
        self.resize(200, 150)

    def open_table_window(self):
        # 創建並顯示表格窗口
        self.table_window = TableWindow()
        self.table_window.show()

class TableWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 創建一個QTableWidget
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setRowCount(5)

        # 填充一些示例數據
        for row in range(5):
            for col in range(3):
                self.table.setItem(row, col, QTableWidgetItem(f"Item {row}, {col}"))

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.setWindowTitle("Table Window")
        self.resize(300, 200)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


