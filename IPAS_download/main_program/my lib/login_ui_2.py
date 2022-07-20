# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from qtwidgets import PasswordEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(490, 251)
        password = PasswordEdit()
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 40, 251, 37))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setToolTipDuration(-1)
        self.label.setScaledContents(False)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 100, 251, 37))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(16)
        self.label_2.setFont(font1)
        self.label_2.setContextMenuPolicy(Qt.NoContextMenu)
        self.label_2.setTextFormat(Qt.PlainText)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(220, 40, 211, 37))
        font2 = QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(12)
        self.lineEdit.setFont(font2)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(190, 160, 111, 41))
        font3 = QFont()
        font3.setFamily(u"Adobe Arabic")
        font3.setPointSize(18)
        self.pushButton.setFont(font3)
        self.lineEdit_2 = QLineEdit(self.centralwidget)    #打密碼
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(220, 100, 211, 37))
        self.lineEdit_2.setFont(font2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 490, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"login", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Username:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"submit", None))
    # retranslateUi

