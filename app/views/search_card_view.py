from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from app.utils.image_loder import get_image_loader


class MediaCard(QWidget):
    """
    Card widget optimized for Dark Backgrounds
    with hover + pressed behavior (Netflix-style).
    """

    clicked = Signal()

    def __init__(
        self,
        title: str,
        cover_url: str,
        description: str,
        released: str,
        item_id: int,
        tmdb_id: int,
        mal_id: int,
        rawg_id: int,
        ol_id: int,
        parent=None
    ):
        super().__init__(parent)
        
        self.item_id = item_id
        self.tmdb_id = tmdb_id
        self.mal_id = mal_id
        self.rawg_id = rawg_id
        self.ol_id = ol_id
        self.cover_url = cover_url
        self.is_pressed = False
        self.image_loader = get_image_loader()

        # IMPORTANT: Object name must match stylesheet
        self.setObjectName("MediaCard")
        self.setCursor(Qt.PointingHandCursor)

        self.setup_ui(title, description, released)
        self.apply_normal_style()

        
        if cover_url:
            self.load_cover_image()

    # ---------------- UI ---------------- #

    def setup_ui(self, title: str, description: str, released: str):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(16)

        # --- Cover Image ---
        self.cover_label = QLabel("...")
        self.cover_label.setObjectName("CoverLabel")
        self.cover_label.setFixedSize(120, 180)
        self.cover_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.cover_label)

        # --- Info Section ---
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        info_layout.setContentsMargins(0, 4, 0, 4)

        # Title
        title_label = QLabel(title or "Unknown Title")
        title_label.setObjectName("TitleLabel")
        title_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title_label.setWordWrap(True)
        info_layout.addWidget(title_label)

        # Released
        if released:
            released_label = QLabel(f"Released: {released}")
            released_label.setObjectName("ReleasedLabel")
            info_layout.addWidget(released_label)

        # Description
        desc_label = QLabel(description or "No description available")
        desc_label.setObjectName("DescLabel")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desc_label.setMaximumHeight(85)
        info_layout.addWidget(desc_label)

        info_layout.addStretch()
        main_layout.addLayout(info_layout)

    # ---------------- Styles ---------------- #

    def apply_normal_style(self):
        self.setStyleSheet("""
            QWidget#MediaCard {
                background-color: #1f2933;
                border-radius: 12px;
                border: 1px solid transparent;
            }

            QWidget#MediaCard:hover {
                background-color: #2a3642;
                border: 1px solid #3b82f6;
            }

            QLabel#CoverLabel {
                background-color: #0f0f15;
                border-radius: 8px;
                color: #555;
            }

            QLabel#TitleLabel {
                color: #ffffff;
            }

            QLabel#ReleasedLabel {
                color: #e94560;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#DescLabel {
                color: #b0b0c0;
                font-size: 13px;
            }
        """)

    def apply_pressed_style(self):
        self.setStyleSheet("""
            QWidget#MediaCard {
                background-color: rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
        """)

    # ---------------- Image ---------------- #

    def load_cover_image(self):
        self.image_loader.load_image(
            url=self.cover_url,
            label=self.cover_label,
            width=120,
            height=180,
            placeholder="...",
            error_text="Img"
        )

    # ---------------- Mouse Events ---------------- #

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_pressed = True
            self.apply_pressed_style()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_pressed:
            self.is_pressed = False
            self.apply_normal_style()
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_pressed and not self.rect().contains(event.pos()):
            self.is_pressed = False
            self.apply_normal_style()
        super().mouseMoveEvent(event)
