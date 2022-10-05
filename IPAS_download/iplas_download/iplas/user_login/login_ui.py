# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(420, 179)
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.password = QLabel(self.centralwidget)
        self.password.setObjectName(u"password")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        self.password.setFont(font1)

        self.gridLayout.addWidget(self.password, 1, 0, 1, 1)

        self.user_input = QLineEdit(self.centralwidget)
        self.user_input.setObjectName(u"user_input")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.user_input.sizePolicy().hasHeightForWidth())
        self.user_input.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"Times New Roman"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.user_input.setFont(font2)

        self.gridLayout.addWidget(self.user_input, 0, 1, 1, 1)

        self.password_input = QLineEdit(self.centralwidget)
        self.password_input.setObjectName(u"password_input")
        font3 = QFont()
        font3.setFamilies([u"Times New Roman"])
        font3.setPointSize(12)
        self.password_input.setFont(font3)

        self.gridLayout.addWidget(self.password_input, 1, 1, 1, 1)

        self.username = QLabel(self.centralwidget)
        self.username.setObjectName(u"username")
        self.username.setFont(font1)

        self.gridLayout.addWidget(self.username, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 5)

        self.login_btm = QPushButton(self.centralwidget)
        self.login_btm.setObjectName(u"login_btm")
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(11)
        self.login_btm.setFont(font4)

        self.gridLayout_2.addWidget(self.login_btm, 2, 2, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font5 = QFont()
        font5.setFamilies([u"\u6a19\u6977\u9ad4"])
        font5.setPointSize(14)
        self.label.setFont(font5)

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 3)

        self.horizontalSpacer = QSpacerItem(88, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 2, 0, 1, 2)

        self.horizontalSpacer_2 = QSpacerItem(88, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 2, 3, 1, 2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 420, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Login", None))
        self.password.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u78bc :", None))
        self.username.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528\u8005\u540d\u7a31 :", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.login_btm.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5165", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8acb\u8f38\u5165OA\u7684\u4f7f\u7528\u8005\u540d\u7a31\u548c\u5bc6\u78bc", None))
    # retranslateUi

