# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_uiRCuXFu.ui'
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
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

from .. import resources_rc

class Ui_show(object):
    def setupUi(self, show):
        if not show.objectName():
            show.setObjectName(u"show")
        show.resize(898, 713)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(show.sizePolicy().hasHeightForWidth())
        show.setSizePolicy(sizePolicy)
        show.setMinimumSize(QSize(674, 713))
        show.setMaximumSize(QSize(1000, 16777215))
        show.setStyleSheet(u"/* ===== SCROLL AREAS & CONTAINERS ===== */\n"
"QScrollArea, QStackedWidget,\n"
"QWidget#scroll_content, \n"
"QWidget#info_scrollarea,\n"
"QWidget#scroll_content_2, \n"
"QWidget#info_scrollarea_2,\n"
"QListWidget#ep_list_widget {\n"
"    background-color: #182126;\n"
"    border: none;\n"
"}\n"
"\n"
"QWidget#show {\n"
"    background-color: #262e39;\n"
"}\n"
"\n"
"/* ===== BASE TEXT STYLES ===== */\n"
"QLabel, QLineEdit, QPushButton, QComboBox {\n"
"    color: #e0e6f0;\n"
"    font-size: 14px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* ===== INPUT FIELDS ===== */\n"
"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.05);\n"
"    padding: 6px;\n"
"    border: none;\n"
"    border-bottom: 1px solid rgba(255, 255, 255, 0.2);\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    background-color: rgba(255, 255, 255, 0.1);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-bottom: 2px solid #5891ff;\n"
"    background-color: rgba(255, 255, 255, 0.12);\n"
"    outline: none;\n"
"}"
                        "\n"
"\n"
"/* ===== BUTTONS ===== */\n"
"QPushButton {\n"
"    background-color: #2e3a4b;\n"
"    border: 1px solid rgba(255, 255, 255, 0.15);\n"
"    border-radius: 6px;\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3c4d63;\n"
"    border: 1px solid #5891ff;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1e2a3a;\n"
"    border: 1px solid #4f7de0;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgba(255, 255, 255, 0.4);\n"
"    background-color: rgba(255, 255, 255, 0.05);\n"
"    border: 1px solid rgba(255, 255, 255, 0.1);\n"
"}\n"
"\n"
"/* ===== COMBO BOXES ===== */\n"
"QComboBox {\n"
"    background-color: rgba(255, 255, 255, 0.05);\n"
"    border: 1px solid rgba(255, 255, 255, 0.15);\n"
"    border-radius: 6px;\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: rgba(255, 255, 255, 0.1);\n"
"    border: 1px solid #5891ff;\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid #5891ff;\n"
"    background-col"
                        "or: rgba(255, 255, 255, 0.12);\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 25px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/Icons/sort_by.png);\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #2e3a4b;\n"
"    color: #e0e6f0;\n"
"    border: 1px solid #5891ff;\n"
"    selection-background-color: #3c4d63;\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"/* ===== TABS ===== */\n"
"QTabWidget::pane {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTabBar {\n"
"    qproperty-drawBase: 0;\n"
"    alignment: center;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: transparent;\n"
"    color: #6d747e;\n"
"    padding: 10px 25px;\n"
"    margin: 0px 5px;\n"
"    font: 13pt \"Segoe UI\";\n"
"    border-bottom: 3px solid transparent;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    color: #cad1d9;\n"
"    border-bottom: "
                        "3px solid #fbffff;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    color: #cad1d9;\n"
"}\n"
"\n"
"/* ===== LABELS ===== */\n"
"QLabel#show_image_lable {\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QDialog {\n"
"    background-color:#182126;    /* your dark color */\n"
"    color: white;\n"
"}\n"
"\n"
"QDialog QLabel {\n"
"    color: white;\n"
"}\n"
"\n"
"\n"
"QScrollArea {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
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
"QScrollBar::sub-line:vert"
                        "ical,\n"
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
"QScrollBar::handle:horizontal:pressed {\n"
"    background: rgba(255, 255, 255, 0.4);\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal,\n"
"QScrollBar::sub-line:horizontal,\n"
"QScrollBar::add-page:horizontal,\n"
"QScrollBar::sub-page:horizontal {\n"
"    background: none;\n"
"    width: 0px;\n"
"}")
        self.gridLayout = QGridLayout(show)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(show)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_4 = QGridLayout(self.tab)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(10, 30, 10, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 10, 20, 5)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ok_button = QPushButton(self.tab)
        self.ok_button.setObjectName(u"ok_button")

        self.horizontalLayout.addWidget(self.ok_button)


        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.scrollArea_2 = QScrollArea(self.tab)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setStyleSheet(u"")
        self.scrollArea_2.setWidgetResizable(True)
        self.info_scrollarea = QWidget()
        self.info_scrollarea.setObjectName(u"info_scrollarea")
        self.info_scrollarea.setGeometry(QRect(0, 0, 870, 1004))
        self.gridLayout_3 = QGridLayout(self.info_scrollarea)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.cover_lable = QLabel(self.info_scrollarea)
        self.cover_lable.setObjectName(u"cover_lable")
        self.cover_lable.setMinimumSize(QSize(180, 270))
        self.cover_lable.setMaximumSize(QSize(180, 270))
        self.cover_lable.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(88, 145, 255, 0.1), stop:1 rgba(255, 255, 255, 0.05));\n"
"border: 2px solid rgba(255, 255, 255, 0.1);\n"
"border-radius: 12px;\n"
"font-size: 11px;\n"
"color: #666;")

        self.horizontalLayout_6.addWidget(self.cover_lable)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 4, -1, -1)
        self.title_lable = QLabel(self.info_scrollarea)
        self.title_lable.setObjectName(u"title_lable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.title_lable.sizePolicy().hasHeightForWidth())
        self.title_lable.setSizePolicy(sizePolicy1)
        self.title_lable.setMaximumSize(QSize(296, 25))
        font = QFont()
        font.setBold(True)
        self.title_lable.setFont(font)
        self.title_lable.setStyleSheet(u"")
        self.title_lable.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.title_lable)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.released_lable = QLabel(self.info_scrollarea)
        self.released_lable.setObjectName(u"released_lable")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.released_lable.sizePolicy().hasHeightForWidth())
        self.released_lable.setSizePolicy(sizePolicy2)
        self.released_lable.setMaximumSize(QSize(1111111, 25))
        self.released_lable.setStyleSheet(u"color: #94a3b8;\n"
"font-size: 14px;\n"
"background: rgba(255, 255, 255, 0.05);\n"
"padding: 6px 12px;\n"
"border-radius: 6px;")
        self.released_lable.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.released_lable)

        self.runtime__lable = QLabel(self.info_scrollarea)
        self.runtime__lable.setObjectName(u"runtime__lable")
        sizePolicy1.setHeightForWidth(self.runtime__lable.sizePolicy().hasHeightForWidth())
        self.runtime__lable.setSizePolicy(sizePolicy1)
        self.runtime__lable.setMaximumSize(QSize(16777215, 25))
        self.runtime__lable.setStyleSheet(u"color: #94a3b8;\n"
"font-size: 14px;\n"
"background: rgba(255, 255, 255, 0.05);\n"
"padding: 6px 12px;\n"
"border-radius: 6px;")
        self.runtime__lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.runtime__lable)

        self.gener_lable = QLabel(self.info_scrollarea)
        self.gener_lable.setObjectName(u"gener_lable")
        sizePolicy1.setHeightForWidth(self.gener_lable.sizePolicy().hasHeightForWidth())
        self.gener_lable.setSizePolicy(sizePolicy1)
        self.gener_lable.setMaximumSize(QSize(16777215, 25))
        self.gener_lable.setStyleSheet(u"color: #94a3b8;\n"
"font-size: 14px;\n"
"background: rgba(255, 255, 255, 0.05);\n"
"padding: 6px 12px;\n"
"border-radius: 6px;")
        self.gener_lable.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.gener_lable)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.trailer_Button = QPushButton(self.info_scrollarea)
        self.trailer_Button.setObjectName(u"trailer_Button")
        self.trailer_Button.setStyleSheet(u"QPushButton {\n"
"                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                    stop:0 #5891ff, stop:1 #7b3ff2);\n"
"                border: none;\n"
"                border-radius: 8px;\n"
"                padding: 12px 24px;\n"
"                color: white;\n"
"                font-size: 14px;\n"
"                font-weight: bold;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                    stop:0 #4a7de0, stop:1 #6a35d9);\n"
"            }")
        icon = QIcon()
        icon.addFile(u":/icons/Icons/file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.trailer_Button.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.trailer_Button)

        self.description_Button = QPushButton(self.info_scrollarea)
        self.description_Button.setObjectName(u"description_Button")
        self.description_Button.setStyleSheet(u"QPushButton {\n"
"                background: rgba(255, 255, 255, 0.1);\n"
"                border: 1px solid rgba(255, 255, 255, 0.2);\n"
"                border-radius: 8px;\n"
"                padding: 12px 24px;\n"
"                color: white;\n"
"                font-size: 14px;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background: rgba(255, 255, 255, 0.15);\n"
"            }")
        self.description_Button.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.description_Button)

        self.favorite_button = QPushButton(self.info_scrollarea)
        self.favorite_button.setObjectName(u"favorite_button")
        self.favorite_button.setMaximumSize(QSize(40, 40))
        self.favorite_button.setAutoFillBackground(False)
        self.favorite_button.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background: rgba(255, 0, 0, 0.1);\n"
"    border-radius: 5px;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/Icons/white_heart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/Icons/blue_heart.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.favorite_button.setIcon(icon1)
        self.favorite_button.setIconSize(QSize(32, 32))
        self.favorite_button.setCheckable(True)
        self.favorite_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.favorite_button)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)

        self.status_combobox = QComboBox(self.info_scrollarea)
        self.status_combobox.setObjectName(u"status_combobox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.status_combobox.sizePolicy().hasHeightForWidth())
        self.status_combobox.setSizePolicy(sizePolicy3)
        self.status_combobox.setMinimumSize(QSize(110, 0))
        self.status_combobox.setMaximumSize(QSize(100, 16777215))
        self.status_combobox.setStyleSheet(u"")
        self.status_combobox.setIconSize(QSize(16, 16))
        self.status_combobox.setFrame(False)

        self.horizontalLayout_7.addWidget(self.status_combobox, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget_4 = QWidget(self.info_scrollarea)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_14 = QVBoxLayout(self.widget_4)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.tmdb_icon_lable = QLabel(self.widget_4)
        self.tmdb_icon_lable.setObjectName(u"tmdb_icon_lable")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tmdb_icon_lable.sizePolicy().hasHeightForWidth())
        self.tmdb_icon_lable.setSizePolicy(sizePolicy4)
        self.tmdb_icon_lable.setMaximumSize(QSize(32, 32))
        self.tmdb_icon_lable.setPixmap(QPixmap(u":/icons/Icons/tmdb.png"))
        self.tmdb_icon_lable.setScaledContents(True)
        self.tmdb_icon_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.tmdb_icon_lable, 0, Qt.AlignmentFlag.AlignHCenter)

        self.tmdb_rating = QLabel(self.widget_4)
        self.tmdb_rating.setObjectName(u"tmdb_rating")
        self.tmdb_rating.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.tmdb_rating)

        self.tmdb_votes = QLabel(self.widget_4)
        self.tmdb_votes.setObjectName(u"tmdb_votes")
        self.tmdb_votes.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.tmdb_votes)


        self.horizontalLayout_2.addWidget(self.widget_4)

        self.widget = QWidget(self.info_scrollarea)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_7 = QVBoxLayout(self.widget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.imdb_icon_lable = QLabel(self.widget)
        self.imdb_icon_lable.setObjectName(u"imdb_icon_lable")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.imdb_icon_lable.sizePolicy().hasHeightForWidth())
        self.imdb_icon_lable.setSizePolicy(sizePolicy5)
        self.imdb_icon_lable.setMaximumSize(QSize(16777215, 16777215))
        self.imdb_icon_lable.setSizeIncrement(QSize(0, 0))
        self.imdb_icon_lable.setAutoFillBackground(False)
        self.imdb_icon_lable.setPixmap(QPixmap(u":/icons/Icons/imdb.png"))
        self.imdb_icon_lable.setScaledContents(False)
        self.imdb_icon_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.imdb_icon_lable)

        self.imdb_rating = QLabel(self.widget)
        self.imdb_rating.setObjectName(u"imdb_rating")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(2)
        sizePolicy6.setHeightForWidth(self.imdb_rating.sizePolicy().hasHeightForWidth())
        self.imdb_rating.setSizePolicy(sizePolicy6)
        self.imdb_rating.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.imdb_rating)

        self.imdb_votes = QLabel(self.widget)
        self.imdb_votes.setObjectName(u"imdb_votes")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(1)
        sizePolicy7.setHeightForWidth(self.imdb_votes.sizePolicy().hasHeightForWidth())
        self.imdb_votes.setSizePolicy(sizePolicy7)
        self.imdb_votes.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.imdb_votes)


        self.horizontalLayout_2.addWidget(self.widget)

        self.user_rating_widget = QWidget(self.info_scrollarea)
        self.user_rating_widget.setObjectName(u"user_rating_widget")
        self.user_rating_widget.setStyleSheet(u"QWidget {\n"
"\n"
"        border: 1px;\n"
"        border-radius: 8px;\n"
"    }\n"
"    QWidget:hover {\n"
"        background-color: #2d2d2d;\n"
"        border: 1px solid #4a4a4a;\n"
"    }\n"
"    QLabel {\n"
"        border: none;\n"
"        background-color: transparent;\n"
"    }")
        self.verticalLayout_8 = QVBoxLayout(self.user_rating_widget)
        self.verticalLayout_8.setSpacing(4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.user_rating_icon_lable = QLabel(self.user_rating_widget)
        self.user_rating_icon_lable.setObjectName(u"user_rating_icon_lable")
        self.user_rating_icon_lable.setStyleSheet(u"border:none")
        self.user_rating_icon_lable.setPixmap(QPixmap(u":/icons/Icons/star.png"))
        self.user_rating_icon_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.user_rating_icon_lable)

        self.user_rating = QLabel(self.user_rating_widget)
        self.user_rating.setObjectName(u"user_rating")
        self.user_rating.setStyleSheet(u"border:none")
        self.user_rating.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.user_rating)


        self.horizontalLayout_2.addWidget(self.user_rating_widget)

        self.widget_5 = QWidget(self.info_scrollarea)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_15 = QVBoxLayout(self.widget_5)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.rottentomato_icon_lable = QLabel(self.widget_5)
        self.rottentomato_icon_lable.setObjectName(u"rottentomato_icon_lable")
        self.rottentomato_icon_lable.setMinimumSize(QSize(32, 32))
        self.rottentomato_icon_lable.setMaximumSize(QSize(16777215, 16777215))
        self.rottentomato_icon_lable.setPixmap(QPixmap(u":/icons/Icons/rotten tomatoes.png"))
        self.rottentomato_icon_lable.setScaledContents(True)

        self.verticalLayout_15.addWidget(self.rottentomato_icon_lable, 0, Qt.AlignmentFlag.AlignHCenter)

        self.rotten_tomatos_rating = QLabel(self.widget_5)
        self.rotten_tomatos_rating.setObjectName(u"rotten_tomatos_rating")
        self.rotten_tomatos_rating.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_15.addWidget(self.rotten_tomatos_rating)


        self.horizontalLayout_2.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.info_scrollarea)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setMinimumSize(QSize(0, 0))
        self.widget_6.setStyleSheet(u"")
        self.verticalLayout_16 = QVBoxLayout(self.widget_6)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.metascore_icon_label = QLabel(self.widget_6)
        self.metascore_icon_label.setObjectName(u"metascore_icon_label")
        self.metascore_icon_label.setMaximumSize(QSize(40, 40))
        self.metascore_icon_label.setPixmap(QPixmap(u":/icons/Icons/metascore.png"))
        self.metascore_icon_label.setScaledContents(True)

        self.verticalLayout_16.addWidget(self.metascore_icon_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.metascore_rating = QLabel(self.widget_6)
        self.metascore_rating.setObjectName(u"metascore_rating")
        self.metascore_rating.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_16.addWidget(self.metascore_rating)


        self.horizontalLayout_2.addWidget(self.widget_6)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.scrollArea_3 = QScrollArea(self.info_scrollarea)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setMinimumSize(QSize(0, 285))
        self.scrollArea_3.setStyleSheet(u"QWidget {\n"
"    background-color: #262e39;\n"
"    border: none;\n"
"}")
        self.scrollArea_3.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea_3.setWidgetResizable(True)
        self.cast_scroll_area = QWidget()
        self.cast_scroll_area.setObjectName(u"cast_scroll_area")
        self.cast_scroll_area.setGeometry(QRect(0, 0, 852, 285))
        self.gridLayout_9 = QGridLayout(self.cast_scroll_area)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.cast_layout = QHBoxLayout()
        self.cast_layout.setObjectName(u"cast_layout")

        self.gridLayout_9.addLayout(self.cast_layout, 0, 0, 1, 1)

        self.scrollArea_3.setWidget(self.cast_scroll_area)

        self.gridLayout_3.addWidget(self.scrollArea_3, 3, 0, 1, 1)

        self.widget_7 = QWidget(self.info_scrollarea)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMinimumSize(QSize(0, 0))
        self.widget_7.setSizeIncrement(QSize(0, 0))
        self.gridLayout_10 = QGridLayout(self.widget_7)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setVerticalSpacing(6)
        self.gridLayout_10.setContentsMargins(-1, 30, -1, -1)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.director_cover_label = QLabel(self.widget_7)
        self.director_cover_label.setObjectName(u"director_cover_label")
        self.director_cover_label.setMinimumSize(QSize(180, 250))
        self.director_cover_label.setMaximumSize(QSize(180, 200))
        self.director_cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.director_cover_label, 0, Qt.AlignmentFlag.AlignTop)

        self.director_name = QLabel(self.widget_7)
        self.director_name.setObjectName(u"director_name")

        self.horizontalLayout_5.addWidget(self.director_name, 0, Qt.AlignmentFlag.AlignTop)


        self.gridLayout_10.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.widget_7, 2, 0, 1, 1)

        self.scrollArea_2.setWidget(self.info_scrollarea)

        self.gridLayout_4.addWidget(self.scrollArea_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_2 = QGridLayout(self.tab_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.tab_3)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Nirmala UI"])
        font1.setBold(True)
        self.label.setFont(font1)

        self.verticalLayout_4.addWidget(self.label)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.find_button_1 = QPushButton(self.tab_3)
        self.find_button_1.setObjectName(u"find_button_1")

        self.verticalLayout_3.addWidget(self.find_button_1)

        self.find_button_2 = QPushButton(self.tab_3)
        self.find_button_2.setObjectName(u"find_button_2")

        self.verticalLayout_3.addWidget(self.find_button_2)

        self.find_button_3 = QPushButton(self.tab_3)
        self.find_button_3.setObjectName(u"find_button_3")

        self.verticalLayout_3.addWidget(self.find_button_3)

        self.find_button_4 = QPushButton(self.tab_3)
        self.find_button_4.setObjectName(u"find_button_4")

        self.verticalLayout_3.addWidget(self.find_button_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_12 = QGridLayout(self.tab_2)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.ep_list_widget = QListWidget(self.tab_2)
        self.ep_list_widget.setObjectName(u"ep_list_widget")
        self.ep_list_widget.setAlternatingRowColors(False)
        self.ep_list_widget.setSpacing(3)

        self.gridLayout_12.addWidget(self.ep_list_widget, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.retranslateUi(show)
        self.ok_button.clicked.connect(show.close)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(show)
    # setupUi

    def retranslateUi(self, show):
        show.setWindowTitle(QCoreApplication.translate("show", u"Form", None))
        self.ok_button.setText(QCoreApplication.translate("show", u"Ok", None))
        self.cover_lable.setText("")
        self.title_lable.setText(QCoreApplication.translate("show", u"The Darknite", None))
        self.released_lable.setText(QCoreApplication.translate("show", u"Date", None))
        self.runtime__lable.setText(QCoreApplication.translate("show", u"Runtime", None))
        self.gener_lable.setText(QCoreApplication.translate("show", u"Gener", None))
        self.trailer_Button.setText(QCoreApplication.translate("show", u"Watch Trailer", None))
        self.description_Button.setText(QCoreApplication.translate("show", u" Read Plot", None))
        self.favorite_button.setText("")
        self.status_combobox.setPlaceholderText(QCoreApplication.translate("show", u"Move to", None))
        self.tmdb_icon_lable.setText("")
        self.tmdb_rating.setText(QCoreApplication.translate("show", u"TMDB Rate", None))
        self.tmdb_votes.setText(QCoreApplication.translate("show", u"votes", None))
        self.imdb_icon_lable.setText("")
        self.imdb_rating.setText(QCoreApplication.translate("show", u"IMDBRate", None))
        self.imdb_votes.setText(QCoreApplication.translate("show", u"votes", None))
        self.user_rating_icon_lable.setText("")
        self.user_rating.setText(QCoreApplication.translate("show", u"User rate", None))
        self.rottentomato_icon_lable.setText("")
        self.rotten_tomatos_rating.setText(QCoreApplication.translate("show", u"roten rate", None))
        self.metascore_icon_label.setText("")
        self.metascore_rating.setText(QCoreApplication.translate("show", u"meta rate", None))
        self.director_cover_label.setText(QCoreApplication.translate("show", u"director Photo", None))
        self.director_name.setText(QCoreApplication.translate("show", u"Director name", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("show", u"Info", None))
        self.label.setText(QCoreApplication.translate("show", u"Find In:-", None))
        self.find_button_1.setText(QCoreApplication.translate("show", u"PushButton", None))
        self.find_button_2.setText(QCoreApplication.translate("show", u"PushButton", None))
        self.find_button_3.setText(QCoreApplication.translate("show", u"PushButton", None))
        self.find_button_4.setText(QCoreApplication.translate("show", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("show", u"Find", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("show", u"Episode", None))
    # retranslateUi

