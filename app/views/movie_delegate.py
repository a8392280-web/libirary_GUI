 # view/movie_delegate.py 
from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPixmap, QColor, QFont, QPainter
from app.utils.image_loder import get_pixmap
from PySide6.QtWidgets import QListView

class MovieDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # Get data
        title = index.data(Qt.UserRole + 1) or "Unknown Title"
        year = index.data(Qt.UserRole + 2) or "N/A"
        pixmap = get_pixmap(index.data(Qt.UserRole + 5))
        
        rect = option.rect
        # Detect current view mode
        is_list_mode = False
        if option.widget and isinstance(option.widget, QListView):
            is_list_mode = option.widget.viewMode() == QListView.ListMode

        # 1. Draw Selection/Hover Background
        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor(60, 120, 216, 80)) # Selection blue
        elif option.state & QStyle.State_MouseOver:
            painter.setBrush(QColor(39, 48, 58, 150))
        else:
            painter.setBrush(Qt.NoBrush)
            
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 8, 8)

        if is_list_mode:
            # --- LIST MODE LAYOUT (Horizontal) ---
            # Poster (Small square-ish)
            poster_rect = QRect(rect.x() + 10, rect.y() + 5, 45, 60)
            if isinstance(pixmap, QPixmap) and not pixmap.isNull():
                painter.drawPixmap(poster_rect, pixmap.scaled(45, 60, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            else:
                painter.setBrush(QColor(34, 34, 34))
                painter.drawRoundedRect(poster_rect, 4, 4)

            # Title & Year side-by-side
            painter.setPen(QColor("#b1bac1"))
            painter.setFont(QFont("Roboto", 11, QFont.Bold))
            # Offset text to the right of the poster
            title_rect = QRect(poster_rect.right() + 15, rect.y(), rect.width() * 0.6, rect.height())
            painter.drawText(title_rect, Qt.AlignVCenter | Qt.AlignLeft, title)

            painter.setPen(QColor("#7a8b99"))
            painter.setFont(QFont("Roboto", 10))
            year_rect = QRect(title_rect.right(), rect.y(), rect.width() - title_rect.right(), rect.height())
            painter.drawText(year_rect.adjusted(0,0,-20,0), Qt.AlignVCenter | Qt.AlignRight, str(year))

        else:
            # --- GRID MODE LAYOUT (Your original vertical card) ---
            poster_rect = QRect(rect.x() + 10, rect.y() + 10, 140, 190)
            if isinstance(pixmap, QPixmap) and not pixmap.isNull():
                painter.drawPixmap(poster_rect, pixmap.scaled(140, 190, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            else:
                painter.setBrush(QColor(34, 34, 34))
                painter.drawRoundedRect(poster_rect, 4, 4)

            painter.setPen(QColor("#b1bac1"))
            painter.setFont(QFont("Roboto", 10, QFont.Bold))
            title_rect = QRect(rect.x() + 10, rect.y() + 205, 140, 30)
            painter.drawText(title_rect, Qt.AlignLeft | Qt.TextWordWrap, title)

            painter.setPen(QColor("#7a8b99"))
            painter.setFont(QFont("Roboto", 9))
            year_rect = QRect(rect.x() + 10, rect.y() + 235, 140, 20)
            painter.drawText(year_rect, Qt.AlignLeft, str(year))

        painter.restore()

    def sizeHint(self, option, index):
        # Check view mode for size as well
        if option.widget and isinstance(option.widget, QListView):
            if option.widget.viewMode() == QListView.ListMode:
                return QSize(option.rect.width(), 70) # Wide but short for rows
        return QSize(160, 260) # Original Grid size