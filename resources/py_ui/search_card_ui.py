from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

class MediaCard(QFrame):
    def __init__(self, title, cover_url, description, released, item_id):
        super().__init__()
        self.setFixedHeight(150)
        self.setObjectName("MediaCard")
        
        # Style to match your UI's dark theme
        self.setStyleSheet("""
            QFrame#MediaCard {
                background-color: #2e3a4b;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            QFrame#MediaCard:hover {
                border: 1px solid #5891ff;
            }
            QLabel { background: transparent; border: none; }
            #Title { color: #ffffff; font-size: 15px; font-weight: bold; }
            #Meta { color: #5891ff; font-size: 11px; }
            #Desc { color: #b0b8c4; font-size: 12px; }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Poster (Left)
        self.poster = QLabel()
        self.poster.setFixedSize(90, 130)
        self.poster.setStyleSheet("background-color: #1e2a3a; border-radius: 4px;")
        self.poster.setScaledContents(True)
        layout.addWidget(self.poster)

        # Info (Right)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("Title")
        self.title_lbl.setWordWrap(True)

        self.meta_lbl = QLabel(f"ID: {item_id}  |  Released: {released}")
        self.meta_lbl.setObjectName("Meta")

        self.desc_lbl = QLabel(description)
        self.desc_lbl.setObjectName("Desc")
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setAlignment(Qt.AlignTop)

        info_layout.addWidget(self.title_lbl)
        info_layout.addWidget(self.meta_lbl)
        info_layout.addWidget(self.desc_lbl, 1)
        
        layout.addLayout(info_layout, 1)

        # Async Image Load
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.set_image)
        self.manager.get(QNetworkRequest(QUrl(cover_url)))

    def set_image(self, reply):
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll())
        if not pixmap.isNull():
            self.poster.setPixmap(pixmap)
        reply.deleteLater()