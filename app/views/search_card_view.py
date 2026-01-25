from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from app.utils.image_loder import get_image_loader


class MediaCard(QWidget):
    """Card widget for displaying media search results"""
    
    # Signal when user wants to add this media
    add_clicked = Signal(int)  # item_id
    clicked = Signal()  # Signal for when the card is clicked

    def __init__(self, title: str, cover_url: str, description: str, 
                 released: str, item_id: int, parent=None):
        super().__init__(parent)
        
        self.item_id = item_id
        self.cover_url = cover_url
        self.image_loader = get_image_loader()
        
        self.setup_ui(title, description, released)
        
        # Load cover image asynchronously
        if cover_url:
            self.load_cover_image()
    
    def setup_ui(self, title: str, description: str, released: str):
        """Setup the card UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2a2a3e;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: #eee;
            }
            QPushButton {
                background-color: #e94560;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d63447;
            }
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        
        # Cover image label
        self.cover_label = QLabel()
        self.cover_label.setFixedSize(100, 150)
        self.cover_label.setStyleSheet("background-color: #1a1a2e; border-radius: 4px;")
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_label.setText("⏳")  # Loading placeholder
        main_layout.addWidget(self.cover_label)
        
        # Info section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        # Title
        title_label = QLabel(title or "Unknown Title")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setWordWrap(True)
        info_layout.addWidget(title_label)
        
        # Released date
        if released:
            released_label = QLabel(f"Released: {released}")
            released_label.setStyleSheet("color: #aaa; font-size: 11px;")
            info_layout.addWidget(released_label)
        
        # Description
        desc_label = QLabel(description or "No description available")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #ccc; font-size: 12px;")
        desc_label.setMaximumHeight(60)
        info_layout.addWidget(desc_label)
        
        info_layout.addStretch()
        
        # Add button
        add_btn = QPushButton("View Details")
        add_btn.clicked.connect(lambda: self.add_clicked.emit(self.item_id))
        info_layout.addWidget(add_btn)
        
        main_layout.addLayout(info_layout, 1)
    
    def load_cover_image(self):
        """Load the cover image asynchronously"""
        self.image_loader.load_image(
            url=self.cover_url,
            label=self.cover_label,
            width=100,
            height=150,
            placeholder="⏳",
            error_text="🖼️"
        )
    def mousePressEvent(self, event):
        """Emit the clicked signal when the card is pressed"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)