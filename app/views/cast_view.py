from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class CastCard(QWidget):
    def __init__(self, name, character, profile_url, load_image_func, parent=None):
        super().__init__(parent)

        self.setFixedWidth(120)
        self.setFixedHeight(220)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Actor image
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 140)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Use your helper function to load the image
        load_image_func(
            url=profile_url,
            label=self.image_label,
            width=self.image_label.width(),
            height=self.image_label.height(),
            placeholder="⏳",
            error_text="🖼️"
        )

        # Actor name
        self.name_label = QLabel(name)
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 10pt;")

        # Character
        self.character_label = QLabel(character)
        self.character_label.setWordWrap(True)
        self.character_label.setAlignment(Qt.AlignCenter)
        self.character_label.setStyleSheet("font-size: 9pt; color: gray;")

        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.character_label)

        self.setLayout(layout)
