# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pdf_UI_2.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(865, 566)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_10 = QGridLayout(self.centralwidget)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
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
        self.address_line = QLineEdit(self.groupBox)
        self.address_line.setObjectName(u"address_line")

        self.gridLayout.addWidget(self.address_line, 1, 1, 1, 3)

        self.number = QLabel(self.groupBox)
        self.number.setObjectName(u"number")
        font = QFont()
        font.setFamilies([u"\u6a19\u6977\u9ad4"])
        font.setPointSize(12)
        self.number.setFont(font)

        self.gridLayout.addWidget(self.number, 0, 0, 1, 1)

        self.address = QLabel(self.groupBox)
        self.address.setObjectName(u"address")
        self.address.setFont(font)

        self.gridLayout.addWidget(self.address, 1, 0, 1, 1)

        self.name_line = QLineEdit(self.groupBox)
        self.name_line.setObjectName(u"name_line")

        self.gridLayout.addWidget(self.name_line, 2, 1, 1, 3)

        self.name = QLabel(self.groupBox)
        self.name.setObjectName(u"name")
        self.name.setFont(font)

        self.gridLayout.addWidget(self.name, 2, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.number_line = QLineEdit(self.groupBox)
        self.number_line.setObjectName(u"number_line")
        font1 = QFont()
        font1.setPointSize(12)
        self.number_line.setFont(font1)

        self.gridLayout.addWidget(self.number_line, 0, 2, 1, 1)

        self.label_V = QLabel(self.groupBox)
        self.label_V.setObjectName(u"label_V")

        self.gridLayout.addWidget(self.label_V, 0, 1, 1, 1)


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

        self.import_btm = QPushButton(self.centralwidget)
        self.import_btm.setObjectName(u"import_btm")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.import_btm.sizePolicy().hasHeightForWidth())
        self.import_btm.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(12)
        self.import_btm.setFont(font2)
        self.import_btm.setMouseTracking(False)

        self.gridLayout_9.addWidget(self.import_btm, 0, 1, 1, 1)

        self.start_btm = QPushButton(self.centralwidget)
        self.start_btm.setObjectName(u"start_btm")
        sizePolicy1.setHeightForWidth(self.start_btm.sizePolicy().hasHeightForWidth())
        self.start_btm.setSizePolicy(sizePolicy1)
        self.start_btm.setFont(font2)

        self.gridLayout_9.addWidget(self.start_btm, 0, 2, 1, 1)

        self.status_txt = QPlainTextEdit(self.centralwidget)
        self.status_txt.setObjectName(u"status_txt")

        self.gridLayout_9.addWidget(self.status_txt, 1, 0, 1, 3)


        self.gridLayout_10.addLayout(self.gridLayout_9, 5, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.gridLayout_8 = QGridLayout(self.tab_1)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tab_1_title_1 = QLabel(self.tab_1)
        self.tab_1_title_1.setObjectName(u"tab_1_title_1")
        self.tab_1_title_1.setFont(font)

        self.verticalLayout.addWidget(self.tab_1_title_1)

        self.tab_1_title_2 = QLabel(self.tab_1)
        self.tab_1_title_2.setObjectName(u"tab_1_title_2")
        self.tab_1_title_2.setFont(font)
        self.tab_1_title_2.setTextFormat(Qt.AutoText)

        self.verticalLayout.addWidget(self.tab_1_title_2)

        self.tab_1_title_3 = QLabel(self.tab_1)
        self.tab_1_title_3.setObjectName(u"tab_1_title_3")
        self.tab_1_title_3.setFont(font)

        self.verticalLayout.addWidget(self.tab_1_title_3)


        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.build_No_input = QLineEdit(self.tab_1)
        self.build_No_input.setObjectName(u"build_No_input")

        self.gridLayout_2.addWidget(self.build_No_input, 1, 4, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(468, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 0, 2, 1, 4)

        self.label_2 = QLabel(self.tab_1)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 5, 1, 1)

        self.build_num = QLabel(self.tab_1)
        self.build_num.setObjectName(u"build_num")

        self.gridLayout_2.addWidget(self.build_num, 1, 1, 1, 1)

        self.muilti = QRadioButton(self.tab_1)
        self.stamp_selection_group = QButtonGroup(MainWindow)
        self.stamp_selection_group.setObjectName(u"stamp_selection_group")
        self.stamp_selection_group.addButton(self.muilti)
        self.muilti.setObjectName(u"muilti")

        self.gridLayout_2.addWidget(self.muilti, 0, 1, 1, 1)

        self.single = QRadioButton(self.tab_1)
        self.stamp_selection_group.addButton(self.single)
        self.single.setObjectName(u"single")

        self.gridLayout_2.addWidget(self.single, 0, 0, 1, 1)

        self.build_num_input = QLineEdit(self.tab_1)
        self.build_num_input.setObjectName(u"build_num_input")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.build_num_input.sizePolicy().hasHeightForWidth())
        self.build_num_input.setSizePolicy(sizePolicy2)
        self.build_num_input.setMinimumSize(QSize(133, 21))

        self.gridLayout_2.addWidget(self.build_num_input, 1, 2, 1, 1)

        self.build_No = QLabel(self.tab_1)
        self.build_No.setObjectName(u"build_No")

        self.gridLayout_2.addWidget(self.build_No, 1, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 1, 0, 1, 2)

        self.horizontalSpacer_6 = QSpacerItem(608, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_6, 2, 0, 1, 1)

        self.config_1_btm = QPushButton(self.tab_1)
        self.config_1_btm.setObjectName(u"config_1_btm")

        self.gridLayout_4.addWidget(self.config_1_btm, 2, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_7 = QGridLayout(self.tab_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tab_2_title_1 = QLabel(self.tab_2)
        self.tab_2_title_1.setObjectName(u"tab_2_title_1")
        self.tab_2_title_1.setFont(font)

        self.verticalLayout_2.addWidget(self.tab_2_title_1)

        self.tab_2_title_2 = QLabel(self.tab_2)
        self.tab_2_title_2.setObjectName(u"tab_2_title_2")
        self.tab_2_title_2.setFont(font)
        self.tab_2_title_2.setTextFormat(Qt.AutoText)

        self.verticalLayout_2.addWidget(self.tab_2_title_2)

        self.tab_2_title_3 = QLabel(self.tab_2)
        self.tab_2_title_3.setObjectName(u"tab_2_title_3")
        self.tab_2_title_3.setFont(font)

        self.verticalLayout_2.addWidget(self.tab_2_title_3)


        self.gridLayout_6.addLayout(self.verticalLayout_2, 0, 0, 1, 2)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer_7 = QSpacerItem(538, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 0, 0, 1, 5)

        self.radioButton_1 = QRadioButton(self.tab_2)
        self.audit_selection_group = QButtonGroup(MainWindow)
        self.audit_selection_group.setObjectName(u"audit_selection_group")
        self.audit_selection_group.addButton(self.radioButton_1)
        self.radioButton_1.setObjectName(u"radioButton_1")

        self.gridLayout_5.addWidget(self.radioButton_1, 1, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.tab_2)
        self.audit_selection_group.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_5.addWidget(self.radioButton_2, 1, 1, 1, 1)

        self.radioButton_3 = QRadioButton(self.tab_2)
        self.audit_selection_group.addButton(self.radioButton_3)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout_5.addWidget(self.radioButton_3, 1, 2, 1, 1)

        self.radioButton_4 = QRadioButton(self.tab_2)
        self.audit_selection_group.addButton(self.radioButton_4)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.gridLayout_5.addWidget(self.radioButton_4, 1, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(78, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 1, 4, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_5, 1, 0, 1, 2)

        self.horizontalSpacer_4 = QSpacerItem(438, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_4, 2, 0, 1, 1)

        self.config_2_btm = QPushButton(self.tab_2)
        self.config_2_btm.setObjectName(u"config_2_btm")

        self.gridLayout_6.addWidget(self.config_2_btm, 2, 1, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_10.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 865, 22))
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
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.number.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.address.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_V.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.file_name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.import_btm.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.start_btm.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.tab_1_title_1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tab_1_title_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tab_1_title_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.build_num.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.muilti.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.single.setText(QCoreApplication.translate("MainWindow", u"Radi", None))
        self.build_No.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.config_1_btm.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tab_2_title_1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tab_2_title_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tab_2_title_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.radioButton_1.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.config_2_btm.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
    # retranslateUi

