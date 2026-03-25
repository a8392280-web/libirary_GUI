# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regesterxcyHom.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModality.NonModal)
        Form.resize(450, 600)
        Form.setMinimumSize(QSize(450, 600))
        Form.setMaximumSize(QSize(450, 600))
        Form.setStyleSheet(u"QWidget {\n"
"                background-color: #1a1a2e;\n"
"                color: #eee;\n"
"                font-family: 'Segoe UI', Arial, sans-serif;\n"
"            }\n"
"            QLineEdit {\n"
"                background-color: #16213e;\n"
"                border: 2px solid #0f3460;\n"
"                border-radius: 8px;\n"
"                padding: 12px;\n"
"                color: #eee;\n"
"                font-size: 14px;\n"
"            }\n"
"            QLineEdit:focus {\n"
"                border: 2px solid #e94560;\n"
"            }\n"
" 	    QPushButton{\n"
"                background-color: #e94560;\n"
"                color: white;\n"
"                border: none;\n"
"                border-radius: 8px;\n"
"                padding: 12px;\n"
"                font-size: 15px;\n"
"                font-weight: bold;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #d63447;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                bac"
                        "kground-color: #c52a3a;\n"
"            }\n"
"            QPushButton:disabled {\n"
"                background-color: #555;\n"
"                color: #888;\n"
"            }\n"
"	    QPushButton#sign_up_switchBtn,\n"
"		QPushButton#login_switchBtn {\n"
"    	background-color: transparent;\n"
"    	color: #e94560;\n"
"    	text-decoration: underline;\n"
"    	padding: 5px;\n"
"}\n"
"QPushButton#sign_up_switchBtn:hover,\n"
"\n"
"QPushButton#verify_back:hove,\n"
"QPushButton#login_switchBtn:hover {\n"
"    color: #d63447;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.sign_up_page = QWidget()
        self.sign_up_page.setObjectName(u"sign_up_page")
        self.verticalLayout_3 = QVBoxLayout(self.sign_up_page)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.label = QLabel(self.sign_up_page)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(30)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_2 = QLabel(self.sign_up_page)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        self.label_2.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 10)
        self.label_3 = QLabel(self.sign_up_page)
        self.label_3.setObjectName(u"label_3")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(12)
        font2.setBold(False)
        self.label_3.setFont(font2)

        self.verticalLayout.addWidget(self.label_3)

        self.sign_up_name_line = QLineEdit(self.sign_up_page)
        self.sign_up_name_line.setObjectName(u"sign_up_name_line")

        self.verticalLayout.addWidget(self.sign_up_name_line)

        self.label_4 = QLabel(self.sign_up_page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.verticalLayout.addWidget(self.label_4)

        self.sign_up_email_line = QLineEdit(self.sign_up_page)
        self.sign_up_email_line.setObjectName(u"sign_up_email_line")

        self.verticalLayout.addWidget(self.sign_up_email_line)

        self.label_5 = QLabel(self.sign_up_page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

        self.verticalLayout.addWidget(self.label_5)

        self.sign_up_password_line = QLineEdit(self.sign_up_page)
        self.sign_up_password_line.setObjectName(u"sign_up_password_line")
        self.sign_up_password_line.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout.addWidget(self.sign_up_password_line)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.sign_up_button = QPushButton(self.sign_up_page)
        self.sign_up_button.setObjectName(u"sign_up_button")

        self.verticalLayout_3.addWidget(self.sign_up_button)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(100, -1, -1, -1)
        self.label_6 = QLabel(self.sign_up_page)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6, 0, Qt.AlignmentFlag.AlignRight)

        self.login_switchBtn = QPushButton(self.sign_up_page)
        self.login_switchBtn.setObjectName(u"login_switchBtn")

        self.horizontalLayout.addWidget(self.login_switchBtn, 0, Qt.AlignmentFlag.AlignLeft)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 3)
        self.verticalLayout_3.setStretch(4, 1)
        self.stackedWidget.addWidget(self.sign_up_page)
        self.login_page = QWidget()
        self.login_page.setObjectName(u"login_page")
        self.verticalLayout_6 = QVBoxLayout(self.login_page)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_10 = QLabel(self.login_page)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.verticalLayout_5.addWidget(self.label_10, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_11 = QLabel(self.login_page)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.verticalLayout_5.addWidget(self.label_11, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_8 = QLabel(self.login_page)
        self.label_8.setObjectName(u"label_8")
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(12)
        self.label_8.setFont(font3)

        self.verticalLayout_4.addWidget(self.label_8)

        self.login_email = QLineEdit(self.login_page)
        self.login_email.setObjectName(u"login_email")

        self.verticalLayout_4.addWidget(self.login_email)

        self.label_7 = QLabel(self.login_page)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font3)

        self.verticalLayout_4.addWidget(self.label_7)

        self.login_password = QLineEdit(self.login_page)
        self.login_password.setObjectName(u"login_password")

        self.verticalLayout_4.addWidget(self.login_password)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)

        self.login_button = QPushButton(self.login_page)
        self.login_button.setObjectName(u"login_button")

        self.verticalLayout_6.addWidget(self.login_button)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(100, -1, -1, -1)
        self.label_9 = QLabel(self.login_page)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_2.addWidget(self.label_9, 0, Qt.AlignmentFlag.AlignRight)

        self.sign_up_switchBtn = QPushButton(self.login_page)
        self.sign_up_switchBtn.setObjectName(u"sign_up_switchBtn")

        self.horizontalLayout_2.addWidget(self.sign_up_switchBtn, 0, Qt.AlignmentFlag.AlignLeft)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)

        self.stackedWidget.addWidget(self.login_page)
        self.verify_page = QWidget()
        self.verify_page.setObjectName(u"verify_page")
        self.verticalLayout_7 = QVBoxLayout(self.verify_page)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_12 = QLabel(self.verify_page)
        self.label_12.setObjectName(u"label_12")
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(15)
        self.label_12.setFont(font4)

        self.verticalLayout_7.addWidget(self.label_12)

        self.verify_email_label = QLabel(self.verify_page)
        self.verify_email_label.setObjectName(u"verify_email_label")
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(13)
        self.verify_email_label.setFont(font5)
        self.verify_email_label.setFrameShape(QFrame.Shape.NoFrame)
        self.verify_email_label.setTextFormat(Qt.TextFormat.AutoText)

        self.verticalLayout_7.addWidget(self.verify_email_label)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verify_code_line = QLineEdit(self.verify_page)
        self.verify_code_line.setObjectName(u"verify_code_line")
        self.verify_code_line.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_3.addWidget(self.verify_code_line)

        self.verify_resend = QPushButton(self.verify_page)
        self.verify_resend.setObjectName(u"verify_resend")
        self.verify_resend.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.verify_resend)

        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_9 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_7.addItem(self.verticalSpacer_9)

        self.verify_button = QPushButton(self.verify_page)
        self.verify_button.setObjectName(u"verify_button")

        self.verticalLayout_7.addWidget(self.verify_button)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_8)

        self.verify_back = QPushButton(self.verify_page)
        self.verify_back.setObjectName(u"verify_back")
        self.verify_back.setStyleSheet(u"")

        self.verticalLayout_7.addWidget(self.verify_back)

        self.stackedWidget.addWidget(self.verify_page)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Create Account", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Sign up to get sarted", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Name", None))
        self.sign_up_name_line.setText("")
        self.sign_up_name_line.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your name", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Email", None))
        self.sign_up_email_line.setText("")
        self.sign_up_email_line.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your Email", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Password", None))
        self.sign_up_password_line.setText("")
        self.sign_up_password_line.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your Password", None))
        self.sign_up_button.setText(QCoreApplication.translate("Form", u"Sign up", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Already have an account?", None))
        self.login_switchBtn.setText(QCoreApplication.translate("Form", u"login", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Welcome Back", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Login Your account", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Email", None))
        self.login_email.setText("")
        self.login_email.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your Email", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Password", None))
        self.login_password.setText("")
        self.login_password.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your Password", None))
        self.login_button.setText(QCoreApplication.translate("Form", u"Login", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Don't have an account?", None))
        self.sign_up_switchBtn.setText(QCoreApplication.translate("Form", u"Sign up", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"We have send a code to:-", None))
        self.verify_email_label.setText("")
        self.verify_code_line.setPlaceholderText(QCoreApplication.translate("Form", u"Enter the code here", None))
        self.verify_resend.setText(QCoreApplication.translate("Form", u"Resend", None))
        self.verify_button.setText(QCoreApplication.translate("Form", u"verify", None))
        self.verify_back.setText(QCoreApplication.translate("Form", u"back", None))
    # retranslateUi

