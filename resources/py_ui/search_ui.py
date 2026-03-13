# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_uibCmyWt.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLineEdit, QListView, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
from .. import resources_rc

class Ui_add_widget(object):
    def setupUi(self, add_widget):
        if not add_widget.objectName():
            add_widget.setObjectName(u"add_widget")
        add_widget.resize(600, 800)
        add_widget.setMinimumSize(QSize(400, 600))
        add_widget.setMaximumSize(QSize(600, 800))
        add_widget.setStyleSheet(u"QLineEdit {\n"
"    color: #e0e6f0; /* light gray text for dark bg */\n"
"    font-size: 14px;\n"
"    background-color: rgba(255, 255, 255, 0.05); /* slightly visible bg for input field */\n"
"    padding: 6px;\n"
"    border: none;\n"
"    border-bottom: 1px solid rgba(255, 255, 255, 0.2); /* soft light line before focus */\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    background-color: rgba(255, 255, 255, 0.1); /* slightly brighter on hover */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    outline: none;\n"
"    border-bottom: 2px solid #5891ff; /* bright blue focus line */\n"
"    background-color: rgba(255, 255, 255, 0.12);\n"
"}\n"
"\n"
"QLabel {\n"
"    border: 1px solid white;   /* White border */\n"
"    border-radius: 6px;        /* Rounded corners (optional) */\n"
"    padding: 4px;              /* Space inside */\n"
"}\n"
"\n"
"QWidget { \n"
"	background-color: #2b3640;\n"
"}\n"
"\n"
"QPushButton {\n"
"    color: #e0e6f0; /* light text */\n"
"    font-size: 14px;\n"
"    background"
                        "-color: #2e3a4b; /* dark gray-blue button */\n"
"    border: 1px solid rgba(255, 255, 255, 0.15);\n"
"    border-radius: 6px;\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3c4d63; /* lighter on hover */\n"
"    border: 1px solid #5891ff; /* subtle blue glow */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1e2a3a; /* darker when pressed */\n"
"    border: 1px solid #4f7de0;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgba(255, 255, 255, 0.4);\n"
"    background-color: rgba(255, 255, 255, 0.05);\n"
"    border: 1px solid rgba(255, 255, 255, 0.1);\n"
"}\n"
"\n"
"QComboBox {\n"
"    color: #e0e6f0; /* light text */\n"
"    font-size: 14px;\n"
"    background-color: rgba(255, 255, 255, 0.05); /* subtle transparent bg */\n"
"    border: 1px solid rgba(255, 255, 255, 0.15);\n"
"    border-radius: 6px;\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: rgba(255, 255, 255, 0.1);\n"
"    border: 1px solid #5891ff; /*"
                        " subtle blue border */\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid #5891ff;\n"
"    background-color: rgba(255, 255, 255, 0.12);\n"
"    outline: none;\n"
"}\n"
"\n"
"/* \u25bc Dropdown arrow */\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 25px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/Icons/sort_by.png); /* replace with your icon */\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"/* Popup (the dropdown list) */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #2e3a4b; /* darker popup background */\n"
"    color: #e0e6f0;\n"
"    border: 1px solid #5891ff;\n"
"    selection-background-color: #3c4d63; /* selected item background */\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"QDialog {\n"
"   color: white;\n"
"   border: none;\n"
"}\n"
"\n"
"QDialog QLabel {\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transp"
                        "arent;\n"
"    width: 8px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: rgba(255, 255, 255, 0.2);\n"
"    min-height: 30px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: rgba(255, 255, 255, 0.3);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:pressed {\n"
"    background: rgba(255, 255, 255, 0.4);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"    height: 0px;\n"
"}\n"
"\n"
"/* Horizontal */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: transparent;\n"
"    height: 8px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgba(255, 255, 255, 0.2);\n"
"    min-width: 30px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal:hover {\n"
"    background: rgba(255, 255, 255, 0.3);\n"
"}\n"
"\n"
"QScrollBar::handle:h"
                        "orizontal:pressed {\n"
"    background: rgba(255, 255, 255, 0.4);\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal,\n"
"QScrollBar::sub-line:horizontal,\n"
"QScrollBar::add-page:horizontal,\n"
"QScrollBar::sub-page:horizontal {\n"
"    background: none;\n"
"    width: 0px;\n"
"}\n"
"\n"
"QListView{border:none}")
        self.gridLayout = QGridLayout(add_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_media_type = QComboBox(add_widget)
        self.search_media_type.addItem("")
        self.search_media_type.addItem("")
        self.search_media_type.addItem("")
        self.search_media_type.addItem("")
        self.search_media_type.addItem("")
        self.search_media_type.addItem("")
        self.search_media_type.setObjectName(u"search_media_type")

        self.horizontalLayout.addWidget(self.search_media_type)

        self.search_line = QLineEdit(add_widget)
        self.search_line.setObjectName(u"search_line")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_line.sizePolicy().hasHeightForWidth())
        self.search_line.setSizePolicy(sizePolicy)
        self.search_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.search_line)

        self.serach_button = QPushButton(add_widget)
        self.serach_button.setObjectName(u"serach_button")

        self.horizontalLayout.addWidget(self.serach_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.search_listView = QListView(add_widget)
        self.search_listView.setObjectName(u"search_listView")

        self.verticalLayout.addWidget(self.search_listView)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(add_widget)

        QMetaObject.connectSlotsByName(add_widget)
    # setupUi

    def retranslateUi(self, add_widget):
        add_widget.setWindowTitle(QCoreApplication.translate("add_widget", u"Form", None))
        self.search_media_type.setItemText(0, QCoreApplication.translate("add_widget", u"Movies", None))
        self.search_media_type.setItemText(1, QCoreApplication.translate("add_widget", u"Series", None))
        self.search_media_type.setItemText(2, QCoreApplication.translate("add_widget", u"Anime", None))
        self.search_media_type.setItemText(3, QCoreApplication.translate("add_widget", u"Games", None))
        self.search_media_type.setItemText(4, QCoreApplication.translate("add_widget", u"Manga", None))
        self.search_media_type.setItemText(5, QCoreApplication.translate("add_widget", u"Books", None))

        self.search_media_type.setPlaceholderText(QCoreApplication.translate("add_widget", u"Media Type", None))
        self.search_line.setPlaceholderText(QCoreApplication.translate("add_widget", u"Search", None))
        self.serach_button.setText(QCoreApplication.translate("add_widget", u"Go", None))
    # retranslateUi

