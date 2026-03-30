# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_uifjTYgh.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QVBoxLayout, QWidget)

from .. import resources_rc

class Ui_main_widget(object):
    def setupUi(self, main_widget):
        if not main_widget.objectName():
            main_widget.setObjectName(u"main_widget")
        main_widget.resize(1170, 838)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_widget.sizePolicy().hasHeightForWidth())
        main_widget.setSizePolicy(sizePolicy)
        main_widget.setMinimumSize(QSize(0, 0))
        main_widget.setMaximumSize(QSize(16777215, 16777215))
        main_widget.setStyleSheet(u"QWidget#main_widget {\n"
"    background-color: rgb(50, 50, 50);\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 10px;\n"
"}")
        self.gridLayout = QGridLayout(main_widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.side_widget = QWidget(main_widget)
        self.side_widget.setObjectName(u"side_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.side_widget.sizePolicy().hasHeightForWidth())
        self.side_widget.setSizePolicy(sizePolicy1)
        self.side_widget.setMaximumSize(QSize(180, 16777215))
        self.side_widget.setStyleSheet(u"/* Sidebar Container */\n"
"QWidget {\n"
"    background-color:#2b3640;\n"
"    border: none;\n"
"}\n"
"\n"
"/* Navigation Buttons */\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: white;\n"
"    text-align: left;\n"
"    border: none;\n"
"    padding:6px 50px 5px 20px;\n"
"    font-size: 14px;\n"
"    font-weight: normal;\n"
"    margin: 0px 0px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(65, 65, 65);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(75, 75, 75);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-top-left-radius: 12px;\n"
"    border-bottom-left-radius: 12px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* Section Headers/Labels */\n"
"QLabel {\n"
"    color: rgb(255, 255, 255);\n"
"    font-size: 15px;\n"
"    font-weight: bold;\n"
"    text-transform: normal;\n"
"    pad"
                        "ding: 8px 0px ;\n"
"    margin-top: 8px;\n"
"}\n"
"\n"
"/* Icon Labels (if you're using QLabel for icons) */\n"
"QLabel#iconLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"    padding: 0px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"/* Separator Line */\n"
"Line {\n"
"    background-color: rgb(70, 70, 70);\n"
"    border: none;\n"
"    max-height: 1px;\n"
"    min-height: 1px;\n"
"	margin: 0px 12px;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(self.side_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 0, 9)
        self.line_3 = QFrame(self.side_widget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.account_layout = QHBoxLayout()
        self.account_layout.setObjectName(u"account_layout")
        self.account_layout.setContentsMargins(0, 0, 0, -1)
        self.name_lable = QLabel(self.side_widget)
        self.name_lable.setObjectName(u"name_lable")

        self.account_layout.addWidget(self.name_lable)

        self.photo_lable = QLabel(self.side_widget)
        self.photo_lable.setObjectName(u"photo_lable")

        self.account_layout.addWidget(self.photo_lable)


        self.verticalLayout.addLayout(self.account_layout)

        self.label_4 = QLabel(self.side_widget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)

        self.verticalLayout.addWidget(self.label_4)

        self.show_movies = QPushButton(self.side_widget)
        self.show_movies.setObjectName(u"show_movies")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.show_movies.sizePolicy().hasHeightForWidth())
        self.show_movies.setSizePolicy(sizePolicy2)
        self.show_movies.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.show_movies.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u":/icons/Icons/film 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/icons/Icons/film.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_movies.setIcon(icon)
        self.show_movies.setIconSize(QSize(23, 23))
        self.show_movies.setCheckable(True)
        self.show_movies.setAutoExclusive(True)
        self.show_movies.setFlat(True)

        self.verticalLayout.addWidget(self.show_movies)

        self.show_series = QPushButton(self.side_widget)
        self.show_series.setObjectName(u"show_series")
        sizePolicy2.setHeightForWidth(self.show_series.sizePolicy().hasHeightForWidth())
        self.show_series.setSizePolicy(sizePolicy2)
        icon1 = QIcon()
        icon1.addFile(u":/icons/Icons/watching 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/Icons/watching.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_series.setIcon(icon1)
        self.show_series.setIconSize(QSize(25, 25))
        self.show_series.setCheckable(True)
        self.show_series.setAutoExclusive(True)
        self.show_series.setFlat(True)

        self.verticalLayout.addWidget(self.show_series)

        self.show_anime = QPushButton(self.side_widget)
        self.show_anime.setObjectName(u"show_anime")
        icon2 = QIcon()
        icon2.addFile(u":/icons/Icons/anime2.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/icons/Icons/anime.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_anime.setIcon(icon2)
        self.show_anime.setIconSize(QSize(32, 32))
        self.show_anime.setCheckable(True)
        self.show_anime.setAutoExclusive(True)
        self.show_anime.setFlat(True)

        self.verticalLayout.addWidget(self.show_anime)

        self.show_games = QPushButton(self.side_widget)
        self.show_games.setObjectName(u"show_games")
        sizePolicy2.setHeightForWidth(self.show_games.sizePolicy().hasHeightForWidth())
        self.show_games.setSizePolicy(sizePolicy2)
        icon3 = QIcon()
        icon3.addFile(u":/icons/Icons/console 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/Icons/console.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_games.setIcon(icon3)
        self.show_games.setIconSize(QSize(25, 25))
        self.show_games.setCheckable(True)
        self.show_games.setAutoExclusive(True)
        self.show_games.setFlat(True)

        self.verticalLayout.addWidget(self.show_games)

        self.show_books = QPushButton(self.side_widget)
        self.show_books.setObjectName(u"show_books")
        sizePolicy2.setHeightForWidth(self.show_books.sizePolicy().hasHeightForWidth())
        self.show_books.setSizePolicy(sizePolicy2)
        icon4 = QIcon()
        icon4.addFile(u":/icons/Icons/book 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon4.addFile(u":/icons/Icons/book.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_books.setIcon(icon4)
        self.show_books.setIconSize(QSize(25, 25))
        self.show_books.setCheckable(True)
        self.show_books.setAutoExclusive(True)
        self.show_books.setFlat(True)

        self.verticalLayout.addWidget(self.show_books)

        self.show_comics = QPushButton(self.side_widget)
        self.show_comics.setObjectName(u"show_comics")
        sizePolicy2.setHeightForWidth(self.show_comics.sizePolicy().hasHeightForWidth())
        self.show_comics.setSizePolicy(sizePolicy2)
        icon5 = QIcon()
        icon5.addFile(u":/icons/Icons/comic 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon5.addFile(u":/icons/Icons/comic.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_comics.setIcon(icon5)
        self.show_comics.setIconSize(QSize(25, 25))
        self.show_comics.setCheckable(True)
        self.show_comics.setAutoExclusive(True)
        self.show_comics.setFlat(True)

        self.verticalLayout.addWidget(self.show_comics)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.line_4 = QFrame(self.side_widget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.label_5 = QLabel(self.side_widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.label_5)

        self.show_home = QPushButton(self.side_widget)
        self.show_home.setObjectName(u"show_home")
        sizePolicy2.setHeightForWidth(self.show_home.sizePolicy().hasHeightForWidth())
        self.show_home.setSizePolicy(sizePolicy2)
        icon6 = QIcon()
        icon6.addFile(u":/icons/Icons/home 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon6.addFile(u":/icons/Icons/home.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_home.setIcon(icon6)
        self.show_home.setIconSize(QSize(25, 25))
        self.show_home.setCheckable(True)
        self.show_home.setAutoExclusive(True)
        self.show_home.setFlat(True)

        self.verticalLayout.addWidget(self.show_home)

        self.show_profile = QPushButton(self.side_widget)
        self.show_profile.setObjectName(u"show_profile")
        sizePolicy2.setHeightForWidth(self.show_profile.sizePolicy().hasHeightForWidth())
        self.show_profile.setSizePolicy(sizePolicy2)
        icon7 = QIcon()
        icon7.addFile(u":/icons/Icons/user 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon7.addFile(u":/icons/Icons/user.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_profile.setIcon(icon7)
        self.show_profile.setIconSize(QSize(25, 25))
        self.show_profile.setCheckable(True)
        self.show_profile.setAutoExclusive(True)
        self.show_profile.setFlat(True)

        self.verticalLayout.addWidget(self.show_profile)

        self.show_dashboard = QPushButton(self.side_widget)
        self.show_dashboard.setObjectName(u"show_dashboard")
        sizePolicy2.setHeightForWidth(self.show_dashboard.sizePolicy().hasHeightForWidth())
        self.show_dashboard.setSizePolicy(sizePolicy2)
        icon8 = QIcon()
        icon8.addFile(u":/icons/Icons/dashboard 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon8.addFile(u":/icons/Icons/dashboard.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        icon8.addFile(u":/icons/Icons/dashboard.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
        self.show_dashboard.setIcon(icon8)
        self.show_dashboard.setIconSize(QSize(30, 30))
        self.show_dashboard.setCheckable(True)
        self.show_dashboard.setAutoExclusive(True)
        self.show_dashboard.setFlat(True)

        self.verticalLayout.addWidget(self.show_dashboard)

        self.show_setting = QPushButton(self.side_widget)
        self.show_setting.setObjectName(u"show_setting")
        sizePolicy2.setHeightForWidth(self.show_setting.sizePolicy().hasHeightForWidth())
        self.show_setting.setSizePolicy(sizePolicy2)
        icon9 = QIcon()
        icon9.addFile(u":/icons/Icons/setting 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon9.addFile(u":/icons/Icons/setting.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.show_setting.setIcon(icon9)
        self.show_setting.setIconSize(QSize(25, 25))
        self.show_setting.setCheckable(True)
        self.show_setting.setAutoExclusive(True)
        self.show_setting.setFlat(True)

        self.verticalLayout.addWidget(self.show_setting)

        self.verticalSpacer = QSpacerItem(143, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.logout = QPushButton(self.side_widget)
        self.logout.setObjectName(u"logout")
        icon10 = QIcon()
        icon10.addFile(u":/icons/Icons/exit 1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon10.addFile(u":/icons/Icons/exit.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.logout.setIcon(icon10)
        self.logout.setIconSize(QSize(25, 25))

        self.verticalLayout.addWidget(self.logout)


        self.gridLayout.addWidget(self.side_widget, 0, 0, 1, 1)

        self.main_body_widget = QWidget(main_widget)
        self.main_body_widget.setObjectName(u"main_body_widget")
        sizePolicy.setHeightForWidth(self.main_body_widget.sizePolicy().hasHeightForWidth())
        self.main_body_widget.setSizePolicy(sizePolicy)
        self.main_body_widget.setStyleSheet(u"QLabel {\n"
"    color: rgb(230, 230, 230);}")
        self.gridLayout_2 = QGridLayout(self.main_body_widget)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stacked_body_Widget = QStackedWidget(self.main_body_widget)
        self.stacked_body_Widget.setObjectName(u"stacked_body_Widget")
        self.stacked_body_Widget.setEnabled(True)
        self.stacked_body_Widget.setStyleSheet(u"QStackedWidget {\n"
"    background-color: #262e39;}\n"
"\n"
"QListWidget{\n"
"	background-color: #182126;\n"
"	border:none;\n"
"}\n"
"\n"
"QListView{\n"
"	background-color: #182126;\n"
"	border:none;\n"
"}\n"
"\n"
"/* Navigation Buttons */\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: white;\n"
"    text-align: middle;\n"
"    border: none;\n"
"    padding: 5px 5px 5px 5px;\n"
"    font-size: 14px;\n"
"    font-weight: normal;\n"
"    border-radius: 6px;\n"
"	margin: 0px 0px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(65, 65, 65);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(79, 79, 79);\n"
"}\n"
"QLineEdit {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #404040;\n"
"    border-radius: 8px;\n"
"    font-size: 14px;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #888888;\n"
"    font-size: 14px;\n"
"    font-style: normal;\n"
"}\n"
"\n"
"\n"
"/* Separator Line */\n"
"Line {\n"
"    background-co"
                        "lor: rgb(70, 70, 70);\n"
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
"    border: 1px solid #5891ff; /* subtle blue border */\n"
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
"    background-color: #2e3a4b; /* dar"
                        "ker popup background */\n"
"    color: #e0e6f0;\n"
"    border: 1px solid #5891ff;\n"
"    selection-background-color: #3c4d63; /* selected item background */\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: none;\n"
"    background:transparent;  /* light clean background */\n"
"}\n"
"\n"
"QTabBar {\n"
"    qproperty-drawBase: 0;\n"
"    alignment: center;  /* center the tabs */\n"
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
"    color: #cad1d9;  /* accent blue */\n"
"    border-bottom: 3px solid #fbffff;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    color: #cad1d9;\n"
"}\n"
"")
        self.welcome_section = QWidget()
        self.welcome_section.setObjectName(u"welcome_section")
        self.welcome_section.setStyleSheet(u"")
        self.gridLayout_3 = QGridLayout(self.welcome_section)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.label_2 = QLabel(self.welcome_section)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)

        self.label = QLabel(self.welcome_section)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Arial Rounded MT"])
        font1.setPointSize(36)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"QLabel {\n"
"    color: rgb(230, 230, 230);}")
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setScaledContents(False)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 1, 0, 1, 1)

        self.stacked_body_Widget.addWidget(self.welcome_section)
        self.movies_section = QWidget()
        self.movies_section.setObjectName(u"movies_section")
        self.movies_section.setStyleSheet(u"")
        self.gridLayout_7 = QGridLayout(self.movies_section)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 10, 5, 10)
        self.side_bar_button = QPushButton(self.movies_section)
        self.side_bar_button.setObjectName(u"side_bar_button")
        self.side_bar_button.setAutoFillBackground(False)
        icon11 = QIcon()
        icon11.addFile(u":/icons/Icons/more.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.side_bar_button.setIcon(icon11)
        self.side_bar_button.setIconSize(QSize(20, 20))
        self.side_bar_button.setCheckable(True)
        self.side_bar_button.setFlat(False)

        self.horizontalLayout_2.addWidget(self.side_bar_button)

        self.title_label = QLabel(self.movies_section)
        self.title_label.setObjectName(u"title_label")
        font2 = QFont()
        font2.setFamilies([u"Arial Rounded MT"])
        font2.setPointSize(20)
        font2.setBold(True)
        self.title_label.setFont(font2)

        self.horizontalLayout_2.addWidget(self.title_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.add_button = QPushButton(self.movies_section)
        self.add_button.setObjectName(u"add_button")
        sizePolicy2.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy2)
        self.add_button.setMinimumSize(QSize(0, 0))
        self.add_button.setMaximumSize(QSize(16777215, 16777215))
        self.add_button.setAutoFillBackground(False)
        self.add_button.setStyleSheet(u"")
        icon12 = QIcon()
        icon12.addFile(u":/icons/Icons/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.add_button.setIcon(icon12)
        self.add_button.setIconSize(QSize(32, 32))
        self.add_button.setFlat(True)

        self.horizontalLayout_2.addWidget(self.add_button)

        self.view_button = QPushButton(self.movies_section)
        self.view_button.setObjectName(u"view_button")
        icon13 = QIcon()
        icon13.addFile(u":/icons/Icons/list.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon13.addFile(u":/icons/Icons/grid.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.view_button.setIcon(icon13)
        self.view_button.setIconSize(QSize(32, 32))
        self.view_button.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.view_button)

        self.sort_button = QComboBox(self.movies_section)
        self.sort_button.setObjectName(u"sort_button")
        self.sort_button.setStyleSheet(u"")
        self.sort_button.setEditable(False)
        self.sort_button.setIconSize(QSize(32, 32))
        self.sort_button.setDuplicatesEnabled(False)
        self.sort_button.setFrame(False)
        self.sort_button.setLabelDrawingMode(QComboBox.LabelDrawingMode.UseStyle)

        self.horizontalLayout_2.addWidget(self.sort_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.tap_widget = QTabWidget(self.movies_section)
        self.tap_widget.setObjectName(u"tap_widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tap_widget.sizePolicy().hasHeightForWidth())
        self.tap_widget.setSizePolicy(sizePolicy3)
        self.tap_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.tap_widget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.tap_widget.setAutoFillBackground(False)
        self.tap_widget.setStyleSheet(u"")
        self.tap_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tap_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tap_widget.setElideMode(Qt.TextElideMode.ElideNone)
        self.tap_widget.setDocumentMode(True)
        self.tap_widget.setTabsClosable(False)
        self.tap_widget.setMovable(False)
        self.tap_widget.setTabBarAutoHide(False)
        self.movies_watching = QWidget()
        self.movies_watching.setObjectName(u"movies_watching")
        self.gridLayout_13 = QGridLayout(self.movies_watching)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 10, -1, -1)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, 0, 5, -1)
        self.search_button_1 = QPushButton(self.movies_watching)
        self.search_button_1.setObjectName(u"search_button_1")
        icon14 = QIcon()
        icon14.addFile(u":/icons/Icons/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.search_button_1.setIcon(icon14)
        self.search_button_1.setIconSize(QSize(32, 32))
        self.search_button_1.setCheckable(True)

        self.horizontalLayout_5.addWidget(self.search_button_1)

        self.search_line_1 = QLineEdit(self.movies_watching)
        self.search_line_1.setObjectName(u"search_line_1")
        self.search_line_1.setMaximumSize(QSize(200, 30))
        self.search_line_1.setStyleSheet(u"")
        self.search_line_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.search_line_1)

        self.line_2 = QFrame(self.movies_watching)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_5.addWidget(self.line_2)

        self.random_button_1 = QPushButton(self.movies_watching)
        self.random_button_1.setObjectName(u"random_button_1")
        self.random_button_1.setAutoFillBackground(False)
        self.random_button_1.setStyleSheet(u"")
        icon15 = QIcon()
        icon15.addFile(u":/icons/Icons/dice.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.random_button_1.setIcon(icon15)
        self.random_button_1.setIconSize(QSize(32, 32))
        self.random_button_1.setFlat(True)

        self.horizontalLayout_5.addWidget(self.random_button_1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.refresh_button_1 = QPushButton(self.movies_watching)
        self.refresh_button_1.setObjectName(u"refresh_button_1")
        icon16 = QIcon()
        icon16.addFile(u":/icons/Icons/refresh.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refresh_button_1.setIcon(icon16)
        self.refresh_button_1.setIconSize(QSize(32, 32))

        self.horizontalLayout_5.addWidget(self.refresh_button_1)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.list_view_1 = QListView(self.movies_watching)
        self.list_view_1.setObjectName(u"list_view_1")

        self.verticalLayout_8.addWidget(self.list_view_1)


        self.gridLayout_13.addLayout(self.verticalLayout_8, 0, 0, 1, 1)

        self.tap_widget.addTab(self.movies_watching, "")
        self.movies_want_to_watch = QWidget()
        self.movies_want_to_watch.setObjectName(u"movies_want_to_watch")
        self.gridLayout_12 = QGridLayout(self.movies_want_to_watch)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 10, -1, -1)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(5, -1, 5, -1)
        self.search_button_2 = QPushButton(self.movies_want_to_watch)
        self.search_button_2.setObjectName(u"search_button_2")
        self.search_button_2.setIcon(icon14)
        self.search_button_2.setIconSize(QSize(32, 32))
        self.search_button_2.setCheckable(True)

        self.horizontalLayout_8.addWidget(self.search_button_2)

        self.search_line_2 = QLineEdit(self.movies_want_to_watch)
        self.search_line_2.setObjectName(u"search_line_2")
        self.search_line_2.setMaximumSize(QSize(200, 30))
        self.search_line_2.setStyleSheet(u"")
        self.search_line_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.search_line_2)

        self.line_5 = QFrame(self.movies_want_to_watch)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_8.addWidget(self.line_5)

        self.random_button_2 = QPushButton(self.movies_want_to_watch)
        self.random_button_2.setObjectName(u"random_button_2")
        self.random_button_2.setAutoFillBackground(False)
        self.random_button_2.setIcon(icon15)
        self.random_button_2.setIconSize(QSize(32, 32))
        self.random_button_2.setFlat(True)

        self.horizontalLayout_8.addWidget(self.random_button_2)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.refresh_button_2 = QPushButton(self.movies_want_to_watch)
        self.refresh_button_2.setObjectName(u"refresh_button_2")
        self.refresh_button_2.setIcon(icon16)
        self.refresh_button_2.setIconSize(QSize(32, 32))

        self.horizontalLayout_8.addWidget(self.refresh_button_2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.list_view_2 = QListView(self.movies_want_to_watch)
        self.list_view_2.setObjectName(u"list_view_2")

        self.verticalLayout_10.addWidget(self.list_view_2)


        self.gridLayout_12.addLayout(self.verticalLayout_10, 0, 0, 1, 1)

        self.tap_widget.addTab(self.movies_want_to_watch, "")
        self.movies_continue_later = QWidget()
        self.movies_continue_later.setObjectName(u"movies_continue_later")
        self.gridLayout_9 = QGridLayout(self.movies_continue_later)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 9, 0, 0)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(5, -1, 5, -1)
        self.search_button_3 = QPushButton(self.movies_continue_later)
        self.search_button_3.setObjectName(u"search_button_3")
        self.search_button_3.setIcon(icon14)
        self.search_button_3.setIconSize(QSize(32, 32))
        self.search_button_3.setCheckable(True)

        self.horizontalLayout_9.addWidget(self.search_button_3)

        self.search_line_3 = QLineEdit(self.movies_continue_later)
        self.search_line_3.setObjectName(u"search_line_3")
        self.search_line_3.setMaximumSize(QSize(200, 30))
        self.search_line_3.setStyleSheet(u"")
        self.search_line_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_9.addWidget(self.search_line_3)

        self.line_7 = QFrame(self.movies_continue_later)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_9.addWidget(self.line_7)

        self.random_button_3 = QPushButton(self.movies_continue_later)
        self.random_button_3.setObjectName(u"random_button_3")
        self.random_button_3.setAutoFillBackground(False)
        self.random_button_3.setIcon(icon15)
        self.random_button_3.setIconSize(QSize(32, 32))
        self.random_button_3.setFlat(True)

        self.horizontalLayout_9.addWidget(self.random_button_3)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)

        self.refresh_button_3 = QPushButton(self.movies_continue_later)
        self.refresh_button_3.setObjectName(u"refresh_button_3")
        self.refresh_button_3.setIcon(icon16)
        self.refresh_button_3.setIconSize(QSize(32, 32))

        self.horizontalLayout_9.addWidget(self.refresh_button_3)


        self.verticalLayout_11.addLayout(self.horizontalLayout_9)

        self.list_view_3 = QListView(self.movies_continue_later)
        self.list_view_3.setObjectName(u"list_view_3")

        self.verticalLayout_11.addWidget(self.list_view_3)


        self.gridLayout_9.addLayout(self.verticalLayout_11, 0, 0, 1, 1)

        self.tap_widget.addTab(self.movies_continue_later, "")
        self.movies_dont_want_to_watch = QWidget()
        self.movies_dont_want_to_watch.setObjectName(u"movies_dont_want_to_watch")
        self.gridLayout_10 = QGridLayout(self.movies_dont_want_to_watch)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(5)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, -1, 5, -1)
        self.search_button_4 = QPushButton(self.movies_dont_want_to_watch)
        self.search_button_4.setObjectName(u"search_button_4")
        self.search_button_4.setIcon(icon14)
        self.search_button_4.setIconSize(QSize(32, 32))
        self.search_button_4.setCheckable(True)

        self.horizontalLayout_10.addWidget(self.search_button_4)

        self.search_line_4 = QLineEdit(self.movies_dont_want_to_watch)
        self.search_line_4.setObjectName(u"search_line_4")
        self.search_line_4.setMaximumSize(QSize(200, 30))
        self.search_line_4.setStyleSheet(u"")
        self.search_line_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.search_line_4)

        self.line_9 = QFrame(self.movies_dont_want_to_watch)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.Shape.VLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_10.addWidget(self.line_9)

        self.random_button_4 = QPushButton(self.movies_dont_want_to_watch)
        self.random_button_4.setObjectName(u"random_button_4")
        self.random_button_4.setAutoFillBackground(False)
        self.random_button_4.setIcon(icon15)
        self.random_button_4.setIconSize(QSize(32, 32))
        self.random_button_4.setFlat(True)

        self.horizontalLayout_10.addWidget(self.random_button_4)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_7)

        self.refresh_button_4 = QPushButton(self.movies_dont_want_to_watch)
        self.refresh_button_4.setObjectName(u"refresh_button_4")
        self.refresh_button_4.setIcon(icon16)
        self.refresh_button_4.setIconSize(QSize(32, 32))

        self.horizontalLayout_10.addWidget(self.refresh_button_4)


        self.verticalLayout_12.addLayout(self.horizontalLayout_10)

        self.list_view_4 = QListView(self.movies_dont_want_to_watch)
        self.list_view_4.setObjectName(u"list_view_4")

        self.verticalLayout_12.addWidget(self.list_view_4)


        self.gridLayout_10.addLayout(self.verticalLayout_12, 0, 0, 1, 1)

        self.tap_widget.addTab(self.movies_dont_want_to_watch, "")
        self.movies_ended = QWidget()
        self.movies_ended.setObjectName(u"movies_ended")
        self.gridLayout_11 = QGridLayout(self.movies_ended)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(5)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(5, -1, 5, -1)
        self.search_button_5 = QPushButton(self.movies_ended)
        self.search_button_5.setObjectName(u"search_button_5")
        self.search_button_5.setIcon(icon14)
        self.search_button_5.setIconSize(QSize(32, 32))
        self.search_button_5.setCheckable(True)

        self.horizontalLayout_11.addWidget(self.search_button_5)

        self.search_line_5 = QLineEdit(self.movies_ended)
        self.search_line_5.setObjectName(u"search_line_5")
        self.search_line_5.setEnabled(True)
        self.search_line_5.setMaximumSize(QSize(200, 30))
        self.search_line_5.setStyleSheet(u"")
        self.search_line_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_11.addWidget(self.search_line_5)

        self.line_11 = QFrame(self.movies_ended)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.Shape.VLine)
        self.line_11.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_11.addWidget(self.line_11)

        self.random_button_5 = QPushButton(self.movies_ended)
        self.random_button_5.setObjectName(u"random_button_5")
        self.random_button_5.setAutoFillBackground(False)
        self.random_button_5.setIcon(icon15)
        self.random_button_5.setIconSize(QSize(32, 32))
        self.random_button_5.setFlat(True)

        self.horizontalLayout_11.addWidget(self.random_button_5)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_8)

        self.refresh_button_5 = QPushButton(self.movies_ended)
        self.refresh_button_5.setObjectName(u"refresh_button_5")
        self.refresh_button_5.setIcon(icon16)
        self.refresh_button_5.setIconSize(QSize(32, 32))

        self.horizontalLayout_11.addWidget(self.refresh_button_5)


        self.verticalLayout_13.addLayout(self.horizontalLayout_11)

        self.list_view_5 = QListView(self.movies_ended)
        self.list_view_5.setObjectName(u"list_view_5")

        self.verticalLayout_13.addWidget(self.list_view_5)


        self.gridLayout_11.addLayout(self.verticalLayout_13, 0, 0, 1, 1)

        self.tap_widget.addTab(self.movies_ended, "")
        self.movies_favorites = QWidget()
        self.movies_favorites.setObjectName(u"movies_favorites")
        self.gridLayout_35 = QGridLayout(self.movies_favorites)
        self.gridLayout_35.setSpacing(0)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.gridLayout_35.setContentsMargins(0, 9, 0, 0)
        self.verticalLayout_33 = QVBoxLayout()
        self.verticalLayout_33.setSpacing(0)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.verticalLayout_33.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setSpacing(5)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(5, -1, 5, -1)
        self.search_button_6 = QPushButton(self.movies_favorites)
        self.search_button_6.setObjectName(u"search_button_6")
        self.search_button_6.setIcon(icon14)
        self.search_button_6.setIconSize(QSize(32, 32))
        self.search_button_6.setCheckable(True)

        self.horizontalLayout_32.addWidget(self.search_button_6)

        self.search_line_6 = QLineEdit(self.movies_favorites)
        self.search_line_6.setObjectName(u"search_line_6")
        self.search_line_6.setMaximumSize(QSize(200, 30))
        self.search_line_6.setStyleSheet(u"")
        self.search_line_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_32.addWidget(self.search_line_6)

        self.line_10 = QFrame(self.movies_favorites)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.Shape.VLine)
        self.line_10.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_32.addWidget(self.line_10)

        self.random_button_6 = QPushButton(self.movies_favorites)
        self.random_button_6.setObjectName(u"random_button_6")
        self.random_button_6.setAutoFillBackground(False)
        self.random_button_6.setIcon(icon15)
        self.random_button_6.setIconSize(QSize(32, 32))
        self.random_button_6.setFlat(True)

        self.horizontalLayout_32.addWidget(self.random_button_6)

        self.horizontalSpacer_33 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_33)

        self.refresh_button_6 = QPushButton(self.movies_favorites)
        self.refresh_button_6.setObjectName(u"refresh_button_6")
        self.refresh_button_6.setIcon(icon16)
        self.refresh_button_6.setIconSize(QSize(32, 32))

        self.horizontalLayout_32.addWidget(self.refresh_button_6)


        self.verticalLayout_33.addLayout(self.horizontalLayout_32)

        self.list_view_6 = QListView(self.movies_favorites)
        self.list_view_6.setObjectName(u"list_view_6")

        self.verticalLayout_33.addWidget(self.list_view_6)


        self.gridLayout_35.addLayout(self.verticalLayout_33, 0, 0, 1, 1)

        self.tap_widget.addTab(self.movies_favorites, "")

        self.verticalLayout_3.addWidget(self.tap_widget)


        self.gridLayout_7.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.stacked_body_Widget.addWidget(self.movies_section)
        self.setting_section = QWidget()
        self.setting_section.setObjectName(u"setting_section")
        self.setting_section.setStyleSheet(u"")
        self.gridLayout_8 = QGridLayout(self.setting_section)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_4, 3, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 2, 1, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_8.addItem(self.verticalSpacer_5, 1, 0, 1, 1)

        self.label_6 = QLabel(self.setting_section)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.gridLayout_8.addWidget(self.label_6, 0, 0, 1, 2)

        self.stacked_body_Widget.addWidget(self.setting_section)

        self.gridLayout_2.addWidget(self.stacked_body_Widget, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.main_body_widget, 0, 1, 1, 1)


        self.retranslateUi(main_widget)
        self.search_button_5.toggled.connect(self.search_line_5.setVisible)
        self.search_button_1.toggled.connect(self.search_line_1.setVisible)
        self.search_button_2.toggled.connect(self.search_line_2.setVisible)
        self.search_button_3.toggled.connect(self.search_line_3.setVisible)
        self.search_button_4.toggled.connect(self.search_line_4.setVisible)
        self.side_bar_button.toggled.connect(self.side_widget.setHidden)
        self.search_button_6.toggled.connect(self.search_line_6.setVisible)

        self.stacked_body_Widget.setCurrentIndex(0)
        self.tap_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(main_widget)
    # setupUi

    def retranslateUi(self, main_widget):
        main_widget.setWindowTitle(QCoreApplication.translate("main_widget", u"Form", None))
        self.name_lable.setText("")
        self.photo_lable.setText("")
        self.label_4.setText(QCoreApplication.translate("main_widget", u"Media", None))
        self.show_movies.setText(QCoreApplication.translate("main_widget", u"   Movies", None))
        self.show_series.setText(QCoreApplication.translate("main_widget", u"  TV Series", None))
        self.show_anime.setText(QCoreApplication.translate("main_widget", u"  Anime", None))
        self.show_games.setText(QCoreApplication.translate("main_widget", u"  Games", None))
        self.show_books.setText(QCoreApplication.translate("main_widget", u"  Books", None))
        self.show_comics.setText(QCoreApplication.translate("main_widget", u"Manga", None))
        self.label_5.setText(QCoreApplication.translate("main_widget", u"Account", None))
        self.show_home.setText(QCoreApplication.translate("main_widget", u"   Home", None))
        self.show_profile.setText(QCoreApplication.translate("main_widget", u"   Profile", None))
        self.show_dashboard.setText(QCoreApplication.translate("main_widget", u"  Dashboard", None))
        self.show_setting.setText(QCoreApplication.translate("main_widget", u"   Settings", None))
        self.logout.setText(QCoreApplication.translate("main_widget", u"Logout", None))
        self.label_2.setText(QCoreApplication.translate("main_widget", u"This app is designed to be your perfect library for (movies, series, games, etc.)", None))
        self.label.setText(QCoreApplication.translate("main_widget", u"Welcome, to your libirary", None))
#if QT_CONFIG(tooltip)
        self.side_bar_button.setToolTip(QCoreApplication.translate("main_widget", u"Show/Hide the menu", None))
#endif // QT_CONFIG(tooltip)
        self.side_bar_button.setText("")
        self.title_label.setText(QCoreApplication.translate("main_widget", u" Movies", None))
#if QT_CONFIG(tooltip)
        self.add_button.setToolTip(QCoreApplication.translate("main_widget", u"Add a new movie", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.add_button.setStatusTip(QCoreApplication.translate("main_widget", u"Add a new movie", None))
#endif // QT_CONFIG(statustip)
        self.add_button.setText("")
#if QT_CONFIG(shortcut)
        self.add_button.setShortcut(QCoreApplication.translate("main_widget", u"+", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.view_button.setToolTip(QCoreApplication.translate("main_widget", u"Veiw", None))
#endif // QT_CONFIG(tooltip)
        self.view_button.setText("")
#if QT_CONFIG(tooltip)
        self.sort_button.setToolTip(QCoreApplication.translate("main_widget", u"Sort list by", None))
#endif // QT_CONFIG(tooltip)
        self.sort_button.setPlaceholderText(QCoreApplication.translate("main_widget", u"Sort By", None))
#if QT_CONFIG(tooltip)
        self.search_button_1.setToolTip(QCoreApplication.translate("main_widget", u"Press to show the search bar ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.search_button_1.setStatusTip(QCoreApplication.translate("main_widget", u"Press to show the search bar ", None))
#endif // QT_CONFIG(statustip)
        self.search_button_1.setText("")
        self.search_line_1.setPlaceholderText(QCoreApplication.translate("main_widget", u"Search (Name or Year)", None))
#if QT_CONFIG(tooltip)
        self.random_button_1.setToolTip(QCoreApplication.translate("main_widget", u"Choose a random movie from this tap", None))
#endif // QT_CONFIG(tooltip)
        self.random_button_1.setText("")
        self.refresh_button_1.setText("")
        self.tap_widget.setTabText(self.tap_widget.indexOf(self.movies_watching), QCoreApplication.translate("main_widget", u" Watching", None))
#if QT_CONFIG(tooltip)
        self.search_button_2.setToolTip(QCoreApplication.translate("main_widget", u"Press to show the search bar ", None))
#endif // QT_CONFIG(tooltip)
        self.search_button_2.setText("")
        self.search_line_2.setPlaceholderText(QCoreApplication.translate("main_widget", u"Search (Name or Year)", None))
#if QT_CONFIG(tooltip)
        self.random_button_2.setToolTip(QCoreApplication.translate("main_widget", u"Choose a random movie from this tap", None))
#endif // QT_CONFIG(tooltip)
        self.random_button_2.setText("")
        self.refresh_button_2.setText("")
        self.tap_widget.setTabText(self.tap_widget.indexOf(self.movies_want_to_watch), QCoreApplication.translate("main_widget", u"Want To Watch", None))
#if QT_CONFIG(tooltip)
        self.search_button_3.setToolTip(QCoreApplication.translate("main_widget", u"Press to show the search bar ", None))
#endif // QT_CONFIG(tooltip)
        self.search_button_3.setText("")
        self.search_line_3.setPlaceholderText(QCoreApplication.translate("main_widget", u"Search (Name or Year)", None))
#if QT_CONFIG(tooltip)
        self.random_button_3.setToolTip(QCoreApplication.translate("main_widget", u"Choose a random movie from this tap", None))
#endif // QT_CONFIG(tooltip)
        self.random_button_3.setText("")
        self.refresh_button_3.setText("")
        self.tap_widget.setTabText(self.tap_widget.indexOf(self.movies_continue_later), QCoreApplication.translate("main_widget", u"Continue Later", None))
#if QT_CONFIG(tooltip)
        self.search_button_4.setToolTip(QCoreApplication.translate("main_widget", u"Press to show the search bar ", None))
#endif // QT_CONFIG(tooltip)
        self.search_button_4.setText("")
        self.search_line_4.setPlaceholderText(QCoreApplication.translate("main_widget", u"Search (Name or Year)", None))
#if QT_CONFIG(tooltip)
        self.random_button_4.setToolTip(QCoreApplication.translate("main_widget", u"Choose a random movie from this tap", None))
#endif // QT_CONFIG(tooltip)
        self.random_button_4.setText("")
        self.refresh_button_4.setText("")
        self.tap_widget.setTabText(self.tap_widget.indexOf(self.movies_dont_want_to_watch), QCoreApplication.translate("main_widget", u"Dont Wnat To Continue", None))
#if QT_CONFIG(tooltip)
        self.search_button_5.setToolTip(QCoreApplication.translate("main_widget", u"Press to show the search bar ", None))
#endif // QT_CONFIG(tooltip)
        self.search_button_5.setText("")
        self.search_line_5.setPlaceholderText(QCoreApplication.translate("main_widget", u"Search (Name or Year)", None))
#if QT_CONFIG(tooltip)
        self.random_button_5.setToolTip(QCoreApplication.translate("main_widget", u"Choose a random movie from this tap", None))
#endif // QT_CONFIG(tooltip)
        self.random_button_5.setText("")
        self.refresh_button_5.setText("")
        self.tap_widget.setTabText(self.tap_widget.indexOf(self.movies_ended), QCoreApplication.translate("main_widget", u"Watched", None))
#if QT_CONFIG(tooltip)
        self.search_button_6.setToolTip(QCoreApplication.translate("main_widget", u"Press to show the search bar ", None))
#endif // QT_CONFIG(tooltip)
        self.search_button_6.setText("")
        self.search_line_6.setPlaceholderText(QCoreApplication.translate("main_widget", u"Search (Name or Year)", None))
#if QT_CONFIG(tooltip)
        self.random_button_6.setToolTip(QCoreApplication.translate("main_widget", u"Choose a random movie from this tap", None))
#endif // QT_CONFIG(tooltip)
        self.random_button_6.setText("")
        self.refresh_button_6.setText("")
        self.tap_widget.setTabText(self.tap_widget.indexOf(self.movies_favorites), QCoreApplication.translate("main_widget", u"Favorites", None))
        self.label_6.setText(QCoreApplication.translate("main_widget", u"Setting", None))
    # retranslateUi

