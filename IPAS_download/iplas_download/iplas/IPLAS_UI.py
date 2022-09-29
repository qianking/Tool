# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'IPLAS_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTimeEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(824, 576)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_8 = QGridLayout(self.centralwidget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout_8.addWidget(self.plainTextEdit, 0, 2, 2, 1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_8.addWidget(self.line_2, 0, 1, 8, 1)

        self.plainTextEdit_2 = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")

        self.gridLayout_8.addWidget(self.plainTextEdit_2, 3, 2, 4, 1)

        self.line_6 = QFrame(self.centralwidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.gridLayout_8.addWidget(self.line_6, 6, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.comboBox_2 = QComboBox(self.groupBox_2)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout_3.addWidget(self.comboBox_2, 0, 0, 1, 3)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 2)

        self.horizontalSpacer_4 = QSpacerItem(258, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 1, 2, 1, 2)

        self.dateEdit = QDateEdit(self.groupBox_2)
        self.dateEdit.setObjectName(u"dateEdit")

        self.gridLayout_3.addWidget(self.dateEdit, 2, 0, 1, 3)

        self.comboBox_3 = QComboBox(self.groupBox_2)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout_3.addWidget(self.comboBox_3, 2, 3, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(268, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 3, 1, 1, 3)

        self.dateEdit_2 = QDateEdit(self.groupBox_2)
        self.dateEdit_2.setObjectName(u"dateEdit_2")

        self.gridLayout_3.addWidget(self.dateEdit_2, 4, 0, 1, 3)

        self.comboBox_4 = QComboBox(self.groupBox_2)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.gridLayout_3.addWidget(self.comboBox_4, 4, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_2, 1, 0, 3, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        self.pushButton.setFont(font1)

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setFont(font1)

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setFont(font1)

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.gridLayout_8.addLayout(self.horizontalLayout_3, 7, 2, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.groupBox_3)
        self.lineEdit.setObjectName(u"lineEdit")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        self.lineEdit.setFont(font2)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton_8 = QPushButton(self.groupBox_3)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout.addWidget(self.pushButton_8)


        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_3, 7, 0, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.pushButton_9 = QPushButton(self.groupBox)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setFont(font1)

        self.gridLayout.addWidget(self.pushButton_9, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(298, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox, 0, 0, 1, 1)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout_8.addWidget(self.line_4, 4, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_7 = QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.timeEdit = QTimeEdit(self.groupBox_4)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setMinimumDateTime(QDateTime(QDate(2000, 12, 30), QTime(0, 0, 0)))

        self.horizontalLayout_2.addWidget(self.timeEdit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.pushButton_6 = QPushButton(self.groupBox_4)
        self.pushButton_6.setObjectName(u"pushButton_6")
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(13)
        self.pushButton_6.setFont(font3)

        self.horizontalLayout_2.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.groupBox_4)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setFont(font3)

        self.horizontalLayout_2.addWidget(self.pushButton_7)


        self.gridLayout_6.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_4, 2, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 824, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u958b\u59cb\u6642\u9593", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u7d50\u675f\u6642\u9593", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Execute", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u27f2", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.timeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"AP hh:mm", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Del", None))
    # retranslateUi

