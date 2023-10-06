import cv2
import matplotlib.pyplot as plt
import numpy as np
import re

# # 读取图像
JPG_Path = r'D:\Qian\Codeing\Tool\LED\test photo\2367258900089_LED Green Upper_20230628190646.jpg'
# """ bgr_image = cv2.imread(JPG_Path)

# # 将图像从 BGR 转换为 HSV
# hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# # 遍历图像的每个像素
# for y in range(79, 109):
#     for x in range(56, 86):
#         # 获取像素的 HSV 值
#         h, s, v = hsv_image[y, x]
        
#         # 在这里进行你需要的操作，例如打印 HSV 值
#         print('Hue:', h, 'Saturation:', s, 'Value:', v) """



""" img = cv2.imread(JPG_Path)
# Convert the original image from BGR to RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Convert the original image from BGR to HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define the green color range in HSV
lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])

# Apply bilateral filtering
bilateral_filtered_img = cv2.bilateralFilter(img, d=15, sigmaColor=75, sigmaSpace=75)

# Convert the filtered image from BGR to HSV
img_hsv_bilateral = cv2.cvtColor(bilateral_filtered_img, cv2.COLOR_BGR2HSV)

# Threshold the HSV image to get only green colors
mask_bilateral = cv2.inRange(img_hsv_bilateral, lower_green, upper_green)

# Find contours in the mask
contours, _ = cv2.findContours(mask_bilateral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Threshold the original HSV image to get only green colors
mask_original = cv2.inRange(img_hsv, lower_green, upper_green)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_original)

# Create a copy of the original image to draw bounding boxes on
img_with_boxes_original = img_rgb.copy()

# For each contour found in the filtered image, draw a rectangle around it on the original image
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 1)

# Display the final result
cv2.imshow("image", img)
cv2.waitKey(0) """

# img = cv2.imread(JPG_Path)
# img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# x, y, side_length = 56, 79, 30

# lower_custom_range = np.array([0, 0, 50])
# upper_custom_range = np.array([360, 255, 255])

# # Threshold the ROI based on the updated HSV range
# roi = img_hsv[y:y+side_length, x:x+side_length]

# # Threshold the ROI based on the provided HSV range
# mask_roi = cv2.inRange(roi, lower_custom_range, upper_custom_range)

# # Count the number of valid pixels in the mask
# valid_pixel_count = cv2.countNonZero(mask_roi)
# average_hsv = cv2.mean(roi, mask=mask_roi)[:3]
# print(valid_pixel_count)
# print(average_hsv)


from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHBoxLayout, QWidget, QHeaderView
from PySide6.QtCore import Qt
import sys

class FreezeTableExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 640, 480)
        self.setWindowTitle('Freeze Row Example')

        layout = QHBoxLayout()

        # Frozen Table (Row 0)
        self.frozen_table = QTableWidget(self)
        self.frozen_table.setRowCount(10)
        self.frozen_table.setColumnCount(1)
        self.frozen_table.setSelectionMode(QTableWidget.NoSelection)
        self.frozen_table.setFocusPolicy(Qt.NoFocus)
        self.frozen_table.horizontalHeader().hide()

        # Main Table
        self.main_table = QTableWidget(self)
        self.main_table.setRowCount(10)
        self.main_table.setColumnCount(4)
        self.main_table.setHorizontalHeaderLabels(['A', 'B', 'C', 'D'])

        layout.addWidget(self.frozen_table)
        layout.addWidget(self.main_table)

        self.setLayout(layout)

        self.frozen_table.horizontalScrollBar().valueChanged.connect(self.sync_scroll)
        self.main_table.horizontalScrollBar().valueChanged.connect(self.sync_scroll)

        # Fill in the data
        for col in range(4):
            self.main_table.insertColumn(self.main_table.columnCount())

            frozen_item = QTableWidgetItem(f"Item {col}")
            self.frozen_table.insertColumn(self.frozen_table.columnCount())
            self.frozen_table.setItem(0, self.frozen_table.columnCount()-1, frozen_item)

            for row in range(10):
                item = QTableWidgetItem(f"Item {row}, {col}")
                self.main_table.setItem(row, col, item)

        # Adjust size and position
        self.frozen_table.setVerticalHeaderLabels(['Frozen'])
        self.frozen_table.resizeRowsToContents()
        self.frozen_table.resize(self.main_table.horizontalHeader().height(), 
                                 self.frozen_table.horizontalHeader().width() + self.frozen_table.rowHeight(0))
        self.frozen_table.move(0, self.main_table.horizontalHeader().height())
        
        self.frozen_table.verticalHeader().setFixedWidth(self.main_table.verticalHeader().width())
        self.frozen_table.verticalHeader().setSectionResizeMode(0, QHeaderView.Fixed)

    def sync_scroll(self):
        sender = self.sender()
        if sender == self.frozen_table.horizontalScrollBar():
            self.main_table.horizontalScrollBar().setValue(self.frozen_table.horizontalScrollBar().value())
        else:
            self.frozen_table.horizontalScrollBar().setValue(self.main_table.horizontalScrollBar().value())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FreezeTableExample()
    window.show()
    sys.exit(app.exec_())









