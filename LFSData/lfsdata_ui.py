# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lfsdata_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(839, 392)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_1 = QLabel(self.centralwidget)
        self.label_1.setObjectName(u"label_1")

        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.table_1 = QTableWidget(self.centralwidget)
        self.table_1.setObjectName(u"table_1")

        self.gridLayout.addWidget(self.table_1, 1, 0, 1, 1)

        self.table_2 = QTableWidget(self.centralwidget)
        self.table_2.setObjectName(u"table_2")

        self.gridLayout.addWidget(self.table_2, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.import_btm = QPushButton(self.centralwidget)
        self.import_btm.setObjectName(u"import_btm")

        self.horizontalLayout_3.addWidget(self.import_btm)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.num_label = QLabel(self.centralwidget)
        self.num_label.setObjectName(u"num_label")

        self.horizontalLayout.addWidget(self.num_label)

        self.num_show = QLineEdit(self.centralwidget)
        self.num_show.setObjectName(u"num_show")

        self.horizontalLayout.addWidget(self.num_show)


        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.floor_label = QLabel(self.centralwidget)
        self.floor_label.setObjectName(u"floor_label")

        self.horizontalLayout_2.addWidget(self.floor_label)

        self.floor_show = QLineEdit(self.centralwidget)
        self.floor_show.setObjectName(u"floor_show")

        self.horizontalLayout_2.addWidget(self.floor_show)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(228, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 2, 0, 1, 2)

        self.status = QTextEdit(self.centralwidget)
        self.status.setObjectName(u"status")

        self.gridLayout_3.addWidget(self.status, 3, 0, 1, 2)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 839, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.import_btm.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.num_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.floor_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

