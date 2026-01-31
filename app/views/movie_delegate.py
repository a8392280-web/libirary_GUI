# view/movie_delegate.py
from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPixmap, QColor, QFont, QPainter
from app.utils.image_loder import get_pixmap

class MovieDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.card_size = QSize(150, 250)
        self.poster_height = 200

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # Get data from the model
        title = index.data(Qt.UserRole + 1)
        year = index.data(Qt.UserRole + 2)
        pixmap = get_pixmap(index.data(Qt.UserRole + 5)) # We store the loaded QPixmap here

        rect = option.rect

        # 1. Draw Hover Background
        if option.state & QStyle.State_MouseOver:
            painter.setBrush(QColor(39, 48, 58, 100))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, 8, 8)

        # 2. Draw Poster (or placeholder if pixmap is None)
        poster_rect = QRect(rect.x() + 5, rect.y() + 5, 140, 190)
        if isinstance(pixmap, QPixmap) and not pixmap.isNull():
            painter.drawPixmap(poster_rect, pixmap.scaled(140, 190, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        else:
            painter.setBrush(QColor(34, 34, 34))
            painter.drawRoundedRect(poster_rect, 4, 4)

        # 3. Draw Title
        painter.setPen(QColor("#b1bac1"))
        painter.setFont(QFont("Roboto", 10, QFont.Bold))
        title_rect = QRect(rect.x() + 5, rect.y() + 200, 140, 30)
        painter.drawText(title_rect, Qt.AlignLeft | Qt.TextWordWrap, title)

        # 4. Draw Year
        painter.setPen(QColor("#7a8b99"))
        painter.setFont(QFont("Roboto", 9))
        year_rect = QRect(rect.x() + 5, rect.y() + 230, 140, 20)
        painter.drawText(year_rect, Qt.AlignLeft, str(year))

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(160, 260)