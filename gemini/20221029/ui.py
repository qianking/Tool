# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLCDNumber, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 890)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setStyleSheet(u"color: rgb(67, 10, 255);\n"
"border-color: rgb(20, 32, 255);\n"
"alternate-background-color: rgb(30, 60, 255);")
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_3, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.checkBox_14 = QCheckBox(self.centralwidget)
        self.checkBox_14.setObjectName(u"checkBox_14")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_14.sizePolicy().hasHeightForWidth())
        self.checkBox_14.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(22)
        self.checkBox_14.setFont(font)

        self.horizontalLayout_14.addWidget(self.checkBox_14)

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.horizontalLayout_14.addWidget(self.label_14)


        self.gridLayout.addLayout(self.horizontalLayout_14, 5, 3, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.checkBox_7 = QCheckBox(self.centralwidget)
        self.checkBox_7.setObjectName(u"checkBox_7")
        sizePolicy.setHeightForWidth(self.checkBox_7.sizePolicy().hasHeightForWidth())
        self.checkBox_7.setSizePolicy(sizePolicy)
        self.checkBox_7.setFont(font)

        self.horizontalLayout_7.addWidget(self.checkBox_7)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_7)


        self.gridLayout.addLayout(self.horizontalLayout_7, 3, 1, 1, 1)

        self.status_4 = QTextEdit(self.centralwidget)
        self.status_4.setObjectName(u"status_4")

        self.gridLayout.addWidget(self.status_4, 2, 3, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.checkBox_9 = QCheckBox(self.centralwidget)
        self.checkBox_9.setObjectName(u"checkBox_9")
        sizePolicy.setHeightForWidth(self.checkBox_9.sizePolicy().hasHeightForWidth())
        self.checkBox_9.setSizePolicy(sizePolicy)
        self.checkBox_9.setFont(font)

        self.horizontalLayout_9.addWidget(self.checkBox_9)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_9)


        self.gridLayout.addLayout(self.horizontalLayout_9, 3, 3, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.checkBox_4 = QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName(u"checkBox_4")
        sizePolicy.setHeightForWidth(self.checkBox_4.sizePolicy().hasHeightForWidth())
        self.checkBox_4.setSizePolicy(sizePolicy)
        self.checkBox_4.setFont(font)

        self.horizontalLayout_4.addWidget(self.checkBox_4)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_4)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 3, 1, 1)

        self.status_19 = QTextEdit(self.centralwidget)
        self.status_19.setObjectName(u"status_19")

        self.gridLayout.addWidget(self.status_19, 8, 3, 1, 1)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.checkBox_20 = QCheckBox(self.centralwidget)
        self.checkBox_20.setObjectName(u"checkBox_20")
        sizePolicy.setHeightForWidth(self.checkBox_20.sizePolicy().hasHeightForWidth())
        self.checkBox_20.setSizePolicy(sizePolicy)
        self.checkBox_20.setFont(font)

        self.horizontalLayout_20.addWidget(self.checkBox_20)

        self.label_20 = QLabel(self.centralwidget)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font)

        self.horizontalLayout_20.addWidget(self.label_20)


        self.gridLayout.addLayout(self.horizontalLayout_20, 7, 4, 1, 1)

        self.status_7 = QTextEdit(self.centralwidget)
        self.status_7.setObjectName(u"status_7")

        self.gridLayout.addWidget(self.status_7, 4, 1, 1, 1)

        self.status_9 = QTextEdit(self.centralwidget)
        self.status_9.setObjectName(u"status_9")

        self.gridLayout.addWidget(self.status_9, 4, 3, 1, 1)

        self.status_20 = QTextEdit(self.centralwidget)
        self.status_20.setObjectName(u"status_20")

        self.gridLayout.addWidget(self.status_20, 8, 4, 1, 1)

        self.status_5 = QTextEdit(self.centralwidget)
        self.status_5.setObjectName(u"status_5")

        self.gridLayout.addWidget(self.status_5, 2, 4, 1, 1)

        self.status_2 = QTextEdit(self.centralwidget)
        self.status_2.setObjectName(u"status_2")

        self.gridLayout.addWidget(self.status_2, 2, 1, 1, 1)

        self.status_13 = QTextEdit(self.centralwidget)
        self.status_13.setObjectName(u"status_13")

        self.gridLayout.addWidget(self.status_13, 6, 2, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.checkBox_6 = QCheckBox(self.centralwidget)
        self.checkBox_6.setObjectName(u"checkBox_6")
        sizePolicy.setHeightForWidth(self.checkBox_6.sizePolicy().hasHeightForWidth())
        self.checkBox_6.setSizePolicy(sizePolicy)
        self.checkBox_6.setFont(font)

        self.horizontalLayout_6.addWidget(self.checkBox_6)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_6)


        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)

        self.status_3 = QTextEdit(self.centralwidget)
        self.status_3.setObjectName(u"status_3")

        self.gridLayout.addWidget(self.status_3, 2, 2, 1, 1)

        self.status_15 = QTextEdit(self.centralwidget)
        self.status_15.setObjectName(u"status_15")

        self.gridLayout.addWidget(self.status_15, 6, 4, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.checkBox_12 = QCheckBox(self.centralwidget)
        self.checkBox_12.setObjectName(u"checkBox_12")
        sizePolicy.setHeightForWidth(self.checkBox_12.sizePolicy().hasHeightForWidth())
        self.checkBox_12.setSizePolicy(sizePolicy)
        self.checkBox_12.setFont(font)

        self.horizontalLayout_12.addWidget(self.checkBox_12)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_12)


        self.gridLayout.addLayout(self.horizontalLayout_12, 5, 1, 1, 1)

        self.status_8 = QTextEdit(self.centralwidget)
        self.status_8.setObjectName(u"status_8")

        self.gridLayout.addWidget(self.status_8, 4, 2, 1, 1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.checkBox_15 = QCheckBox(self.centralwidget)
        self.checkBox_15.setObjectName(u"checkBox_15")
        sizePolicy.setHeightForWidth(self.checkBox_15.sizePolicy().hasHeightForWidth())
        self.checkBox_15.setSizePolicy(sizePolicy)
        self.checkBox_15.setFont(font)

        self.horizontalLayout_15.addWidget(self.checkBox_15)

        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.horizontalLayout_15.addWidget(self.label_15)


        self.gridLayout.addLayout(self.horizontalLayout_15, 5, 4, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.checkBox_13 = QCheckBox(self.centralwidget)
        self.checkBox_13.setObjectName(u"checkBox_13")
        sizePolicy.setHeightForWidth(self.checkBox_13.sizePolicy().hasHeightForWidth())
        self.checkBox_13.setSizePolicy(sizePolicy)
        self.checkBox_13.setFont(font)

        self.horizontalLayout_13.addWidget(self.checkBox_13)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.horizontalLayout_13.addWidget(self.label_13)


        self.gridLayout.addLayout(self.horizontalLayout_13, 5, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox_1 = QCheckBox(self.centralwidget)
        self.checkBox_1.setObjectName(u"checkBox_1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBox_1.sizePolicy().hasHeightForWidth())
        self.checkBox_1.setSizePolicy(sizePolicy1)
        self.checkBox_1.setFont(font)

        self.horizontalLayout.addWidget(self.checkBox_1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.checkBox_19 = QCheckBox(self.centralwidget)
        self.checkBox_19.setObjectName(u"checkBox_19")
        sizePolicy.setHeightForWidth(self.checkBox_19.sizePolicy().hasHeightForWidth())
        self.checkBox_19.setSizePolicy(sizePolicy)
        self.checkBox_19.setFont(font)

        self.horizontalLayout_19.addWidget(self.checkBox_19)

        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font)

        self.horizontalLayout_19.addWidget(self.label_19)


        self.gridLayout.addLayout(self.horizontalLayout_19, 7, 3, 1, 1)

        self.status_1 = QTextEdit(self.centralwidget)
        self.status_1.setObjectName(u"status_1")

        self.gridLayout.addWidget(self.status_1, 2, 0, 1, 1)

        self.status_6 = QTextEdit(self.centralwidget)
        self.status_6.setObjectName(u"status_6")

        self.gridLayout.addWidget(self.status_6, 4, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.checkBox_10 = QCheckBox(self.centralwidget)
        self.checkBox_10.setObjectName(u"checkBox_10")
        sizePolicy.setHeightForWidth(self.checkBox_10.sizePolicy().hasHeightForWidth())
        self.checkBox_10.setSizePolicy(sizePolicy)
        self.checkBox_10.setFont(font)

        self.horizontalLayout_10.addWidget(self.checkBox_10)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_10)


        self.gridLayout.addLayout(self.horizontalLayout_10, 3, 4, 1, 1)

        self.status_11 = QTextEdit(self.centralwidget)
        self.status_11.setObjectName(u"status_11")

        self.gridLayout.addWidget(self.status_11, 6, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.checkBox_8 = QCheckBox(self.centralwidget)
        self.checkBox_8.setObjectName(u"checkBox_8")
        sizePolicy.setHeightForWidth(self.checkBox_8.sizePolicy().hasHeightForWidth())
        self.checkBox_8.setSizePolicy(sizePolicy)
        self.checkBox_8.setFont(font)

        self.horizontalLayout_8.addWidget(self.checkBox_8)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_8)


        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 2, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.checkBox_17 = QCheckBox(self.centralwidget)
        self.checkBox_17.setObjectName(u"checkBox_17")
        sizePolicy.setHeightForWidth(self.checkBox_17.sizePolicy().hasHeightForWidth())
        self.checkBox_17.setSizePolicy(sizePolicy)
        self.checkBox_17.setFont(font)

        self.horizontalLayout_17.addWidget(self.checkBox_17)

        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)

        self.horizontalLayout_17.addWidget(self.label_17)


        self.gridLayout.addLayout(self.horizontalLayout_17, 7, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        sizePolicy.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy)
        self.checkBox_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.checkBox_2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.status_12 = QTextEdit(self.centralwidget)
        self.status_12.setObjectName(u"status_12")

        self.gridLayout.addWidget(self.status_12, 6, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")
        sizePolicy.setHeightForWidth(self.checkBox_3.sizePolicy().hasHeightForWidth())
        self.checkBox_3.setSizePolicy(sizePolicy)
        self.checkBox_3.setFont(font)

        self.horizontalLayout_3.addWidget(self.checkBox_3)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_3)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 2, 1, 1)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.checkBox_18 = QCheckBox(self.centralwidget)
        self.checkBox_18.setObjectName(u"checkBox_18")
        sizePolicy.setHeightForWidth(self.checkBox_18.sizePolicy().hasHeightForWidth())
        self.checkBox_18.setSizePolicy(sizePolicy)
        self.checkBox_18.setFont(font)

        self.horizontalLayout_18.addWidget(self.checkBox_18)

        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.horizontalLayout_18.addWidget(self.label_18)


        self.gridLayout.addLayout(self.horizontalLayout_18, 7, 2, 1, 1)

        self.status_17 = QTextEdit(self.centralwidget)
        self.status_17.setObjectName(u"status_17")

        self.gridLayout.addWidget(self.status_17, 8, 1, 1, 1)

        self.status_14 = QTextEdit(self.centralwidget)
        self.status_14.setObjectName(u"status_14")

        self.gridLayout.addWidget(self.status_14, 6, 3, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.checkBox_11 = QCheckBox(self.centralwidget)
        self.checkBox_11.setObjectName(u"checkBox_11")
        sizePolicy.setHeightForWidth(self.checkBox_11.sizePolicy().hasHeightForWidth())
        self.checkBox_11.setSizePolicy(sizePolicy)
        self.checkBox_11.setFont(font)

        self.horizontalLayout_11.addWidget(self.checkBox_11)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_11)


        self.gridLayout.addLayout(self.horizontalLayout_11, 5, 0, 1, 1)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.checkBox_16 = QCheckBox(self.centralwidget)
        self.checkBox_16.setObjectName(u"checkBox_16")
        sizePolicy.setHeightForWidth(self.checkBox_16.sizePolicy().hasHeightForWidth())
        self.checkBox_16.setSizePolicy(sizePolicy)
        self.checkBox_16.setFont(font)

        self.horizontalLayout_16.addWidget(self.checkBox_16)

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.horizontalLayout_16.addWidget(self.label_16)


        self.gridLayout.addLayout(self.horizontalLayout_16, 7, 0, 1, 1)

        self.status_10 = QTextEdit(self.centralwidget)
        self.status_10.setObjectName(u"status_10")

        self.gridLayout.addWidget(self.status_10, 4, 4, 1, 1)

        self.status_16 = QTextEdit(self.centralwidget)
        self.status_16.setObjectName(u"status_16")

        self.gridLayout.addWidget(self.status_16, 8, 0, 1, 1)

        self.status_18 = QTextEdit(self.centralwidget)
        self.status_18.setObjectName(u"status_18")

        self.gridLayout.addWidget(self.status_18, 8, 2, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 0, 2, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.checkBox_5 = QCheckBox(self.centralwidget)
        self.checkBox_5.setObjectName(u"checkBox_5")
        sizePolicy.setHeightForWidth(self.checkBox_5.sizePolicy().hasHeightForWidth())
        self.checkBox_5.setSizePolicy(sizePolicy)
        self.checkBox_5.setFont(font)

        self.horizontalLayout_5.addWidget(self.checkBox_5)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_5)


        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 4, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setStyleSheet(u"color: rgb(67, 10, 255);\n"
"border-color: rgb(20, 32, 255);\n"
"alternate-background-color: rgb(30, 60, 255);")
        self.line_4.setLineWidth(2)
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_4, 3, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_serial = QLabel(self.centralwidget)
        self.label_serial.setObjectName(u"label_serial")
        font1 = QFont()
        font1.setFamilies([u"Adobe Arabic"])
        font1.setPointSize(20)
        self.label_serial.setFont(font1)

        self.gridLayout_2.addWidget(self.label_serial, 0, 1, 1, 1)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")
        self.label_time.setFont(font1)

        self.gridLayout_2.addWidget(self.label_time, 1, 1, 1, 1)

        self.test_time = QLabel(self.centralwidget)
        self.test_time.setObjectName(u"test_time")
        font2 = QFont()
        font2.setFamilies([u"Adobe Arabic"])
        font2.setPointSize(24)
        self.test_time.setFont(font2)
        self.test_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.test_time, 1, 0, 1, 1)

        self.serial_name = QLabel(self.centralwidget)
        self.serial_name.setObjectName(u"serial_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.serial_name.sizePolicy().hasHeightForWidth())
        self.serial_name.setSizePolicy(sizePolicy2)
        self.serial_name.setFont(font2)
        self.serial_name.setLayoutDirection(Qt.LeftToRight)
        self.serial_name.setTextFormat(Qt.AutoText)
        self.serial_name.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.serial_name, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.gridLayout_2.addLayout(self.gridLayout_3, 4, 1, 1, 1)

        self.Online_lebal = QLabel(self.centralwidget)
        self.Online_lebal.setObjectName(u"Online_lebal")
        self.Online_lebal.setFont(font2)
        self.Online_lebal.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.Online_lebal, 2, 0, 1, 1)

        self.Online_line = QLabel(self.centralwidget)
        self.Online_line.setObjectName(u"Online_line")
        self.Online_line.setFont(font1)

        self.gridLayout_2.addWidget(self.Online_line, 2, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 4, 2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 3, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 28, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 3, 3, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 28, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 2, 1, 2, 1)

        self.lcdNumber = QLCDNumber(self.centralwidget)
        self.lcdNumber.setObjectName(u"lcdNumber")

        self.gridLayout_4.addWidget(self.lcdNumber, 0, 4, 2, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 2, 4, 1, 1)

        self.start_btm = QPushButton(self.centralwidget)
        self.start_btm.setObjectName(u"start_btm")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.start_btm.sizePolicy().hasHeightForWidth())
        self.start_btm.setSizePolicy(sizePolicy3)
        self.start_btm.setFont(font2)

        self.gridLayout_4.addWidget(self.start_btm, 0, 2, 3, 2)


        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ORT Test", None))
        self.checkBox_14.setText("")
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"14", None))
        self.checkBox_7.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.checkBox_9.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.checkBox_4.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.checkBox_20.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.checkBox_6.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.checkBox_12.setText("")
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"12", None))
        self.checkBox_15.setText("")
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.checkBox_13.setText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"13", None))
        self.checkBox_1.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.checkBox_19.setText("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"19", None))
        self.checkBox_10.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.checkBox_8.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.checkBox_17.setText("")
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"17", None))
        self.checkBox_2.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.checkBox_3.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.checkBox_18.setText("")
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"18", None))
        self.checkBox_11.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"11", None))
        self.checkBox_16.setText("")
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"16", None))
        self.checkBox_5.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_serial.setText("")
        self.label_time.setText("")
        self.test_time.setText(QCoreApplication.translate("MainWindow", u"Test time : ", None))
        self.serial_name.setText(QCoreApplication.translate("MainWindow", u"Serial :", None))
        self.Online_lebal.setText(QCoreApplication.translate("MainWindow", u"Online : ", None))
        self.Online_line.setText("")
        self.start_btm.setText(QCoreApplication.translate("MainWindow", u"\u958b\u59cb", None))
    # retranslateUi

