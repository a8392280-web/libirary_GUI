# view/movie_delegate.py
from PySide6.QtWidgets import QStyledItemDelegate, QStyle, QListView
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPixmap, QColor, QFont, QPainter
from app.utils.image_loader import get_pixmap, get_image_loader  # ✅ Fixed typo


class MediaDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ✅ When any image finishes downloading, repaint all views using this delegate
        get_image_loader().image_loaded.connect(self._on_image_loaded)

    def _on_image_loaded(self, url: str, success: bool):
        """Triggers a repaint on the parent view when an image finishes downloading."""
        if not success:
            return
        # Find the view this delegate is attached to and repaint it
        parent = self.parent()
        if parent and hasattr(parent, 'viewport'):
            parent.viewport().update()

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
            painter.setBrush(QColor(60, 120, 216, 80))
        elif option.state & QStyle.State_MouseOver:
            painter.setBrush(QColor(39, 48, 58, 150))
        else:
            painter.setBrush(Qt.NoBrush)

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 8, 8)

        if is_list_mode:
            # --- LIST MODE LAYOUT (Horizontal) ---
            poster_rect = QRect(rect.x() + 10, rect.y() + 5, 45, 60)
            if isinstance(pixmap, QPixmap) and not pixmap.isNull():
                painter.drawPixmap(
                    poster_rect,
                    pixmap.scaled(45, 60, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                )
            else:
                painter.setBrush(QColor(34, 34, 34))
                painter.drawRoundedRect(poster_rect, 4, 4)

            painter.setPen(QColor("#b1bac1"))
            painter.setFont(QFont("Roboto", 11, QFont.Bold))
            title_rect = QRect(poster_rect.right() + 15, rect.y(), rect.width() * 0.6, rect.height())
            painter.drawText(title_rect, Qt.AlignVCenter | Qt.AlignLeft, title)

            painter.setPen(QColor("#7a8b99"))
            painter.setFont(QFont("Roboto", 10))
            year_rect = QRect(title_rect.right(), rect.y(), rect.width() - title_rect.right(), rect.height())
            painter.drawText(year_rect.adjusted(0, 0, -20, 0), Qt.AlignVCenter | Qt.AlignRight, str(year))

        else:
            # --- GRID MODE LAYOUT (Vertical card) ---
            poster_rect = QRect(rect.x() + 10, rect.y() + 10, 140, 190)
            if isinstance(pixmap, QPixmap) and not pixmap.isNull():
                painter.drawPixmap(
                    poster_rect,
                    pixmap.scaled(140, 190, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                )
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
        if option.widget and isinstance(option.widget, QListView):
            if option.widget.viewMode() == QListView.ListMode:
                return QSize(option.rect.width(), 70)
        return QSize(160, 260)