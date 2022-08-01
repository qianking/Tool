# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pdf_UI_2.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPlainTextEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(760, 494)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_10 = QGridLayout(self.centralwidget)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_4 = QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(self.tab)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setFamilies([u"\u6a19\u6977\u9ad4"])
        font.setPointSize(12)
        self.title.setFont(font)

        self.verticalLayout.addWidget(self.title)

        self.title_1 = QLabel(self.tab)
        self.title_1.setObjectName(u"title_1")
        self.title_1.setFont(font)
        self.title_1.setTextFormat(Qt.AutoText)

        self.verticalLayout.addWidget(self.title_1)

        self.title_2 = QLabel(self.tab)
        self.title_2.setObjectName(u"title_2")
        self.title_2.setFont(font)

        self.verticalLayout.addWidget(self.title_2)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 2)

        self.horizontalSpacer_3 = QSpacerItem(438, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 1, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_6 = QGridLayout(self.tab_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.title_4 = QLabel(self.tab_2)
        self.title_4.setObjectName(u"title_4")
        self.title_4.setFont(font)

        self.verticalLayout_2.addWidget(self.title_4)

        self.title_5 = QLabel(self.tab_2)
        self.title_5.setObjectName(u"title_5")
        self.title_5.setFont(font)
        self.title_5.setTextFormat(Qt.AutoText)

        self.verticalLayout_2.addWidget(self.title_5)

        self.title_3 = QLabel(self.tab_2)
        self.title_3.setObjectName(u"title_3")
        self.title_3.setFont(font)

        self.verticalLayout_2.addWidget(self.title_3)


        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 6)

        self.radioButton = QRadioButton(self.tab_2)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout_5.addWidget(self.radioButton, 1, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.tab_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_5.addWidget(self.radioButton_2, 1, 1, 1, 1)

        self.radioButton_3 = QRadioButton(self.tab_2)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout_5.addWidget(self.radioButton_3, 1, 2, 1, 1)

        self.radioButton_4 = QRadioButton(self.tab_2)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.gridLayout_5.addWidget(self.radioButton_4, 1, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 1, 4, 1, 1)

        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_5.addWidget(self.pushButton_2, 1, 5, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_8 = QGridLayout(self.tab_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.title_6 = QLabel(self.tab_3)
        self.title_6.setObjectName(u"title_6")
        self.title_6.setFont(font)

        self.verticalLayout_3.addWidget(self.title_6)

        self.title_7 = QLabel(self.tab_3)
        self.title_7.setObjectName(u"title_7")
        self.title_7.setFont(font)
        self.title_7.setTextFormat(Qt.AutoText)

        self.verticalLayout_3.addWidget(self.title_7)

        self.title_8 = QLabel(self.tab_3)
        self.title_8.setObjectName(u"title_8")
        self.title_8.setFont(font)

        self.verticalLayout_3.addWidget(self.title_8)


        self.gridLayout_7.addLayout(self.verticalLayout_3, 0, 0, 1, 2)

        self.horizontalSpacer_5 = QSpacerItem(598, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.tab_3)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_7.addWidget(self.pushButton_3, 1, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout_10.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_10.addWidget(self.line_2, 1, 0, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.number = QLabel(self.groupBox)
        self.number.setObjectName(u"number")
        self.number.setFont(font)

        self.gridLayout.addWidget(self.number, 0, 0, 1, 1)

        self.name = QLabel(self.groupBox)
        self.name.setObjectName(u"name")
        self.name.setFont(font)

        self.gridLayout.addWidget(self.name, 2, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.address = QLabel(self.groupBox)
        self.address.setObjectName(u"address")
        self.address.setFont(font)

        self.gridLayout.addWidget(self.address, 1, 0, 1, 1)

        self.address_line = QLineEdit(self.groupBox)
        self.address_line.setObjectName(u"address_line")

        self.gridLayout.addWidget(self.address_line, 1, 1, 1, 2)

        self.name_line = QLineEdit(self.groupBox)
        self.name_line.setObjectName(u"name_line")

        self.gridLayout.addWidget(self.name_line, 2, 1, 1, 2)

        self.number_line = QLineEdit(self.groupBox)
        self.number_line.setObjectName(u"number_line")

        self.gridLayout.addWidget(self.number_line, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.file_name = QLabel(self.centralwidget)
        self.file_name.setObjectName(u"file_name")
        self.file_name.setFont(font)

        self.horizontalLayout.addWidget(self.file_name)

        self.file_name_line = QLineEdit(self.centralwidget)
        self.file_name_line.setObjectName(u"file_name_line")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_name_line.sizePolicy().hasHeightForWidth())
        self.file_name_line.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.file_name_line)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(12)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)


        self.gridLayout_10.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_10.addWidget(self.line, 4, 0, 1, 1)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalSpacer = QSpacerItem(458, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.impoer_btm = QPushButton(self.centralwidget)
        self.impoer_btm.setObjectName(u"impoer_btm")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.impoer_btm.sizePolicy().hasHeightForWidth())
        self.impoer_btm.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(12)
        self.impoer_btm.setFont(font2)
        self.impoer_btm.setMouseTracking(False)

        self.gridLayout_9.addWidget(self.impoer_btm, 0, 1, 1, 1)

        self.start_btm = QPushButton(self.centralwidget)
        self.start_btm.setObjectName(u"start_btm")
        sizePolicy1.setHeightForWidth(self.start_btm.sizePolicy().hasHeightForWidth())
        self.start_btm.setSizePolicy(sizePolicy1)
        self.start_btm.setFont(font2)

        self.gridLayout_9.addWidget(self.start_btm, 0, 2, 1, 1)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout_9.addWidget(self.plainTextEdit, 1, 0, 1, 3)


        self.gridLayout_10.addLayout(self.gridLayout_9, 5, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 760, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.title_1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.title_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.title_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.title_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.title_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.title_6.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.title_7.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.title_8.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u9801\u9762", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.number.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.address.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.file_name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.impoer_btm.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.start_btm.setText(QCoreApplication.translate("MainWindow", u"Start", None))
    # retranslateUi

