from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, Signal
from resources.py_ui.search_ui import Ui_add_widget
from app.views.search_card_view import MediaCard


class SearchView(QDialog):
    """Pure UI component for search dialog"""
    
    # Signals for user actions
    search_requested = Signal(str, str, str)  # query, media_type, source
    source_changed = Signal(int)  # source index
    text_changed = Signal(str)  # search text
    
    def __init__(self):
        super().__init__()
        # Setup UI
        self.ui = Ui_add_widget()
        self.ui.setupUi(self)
        
        # Set alignment and spacing
        self.ui.search_verticallayout.setAlignment(Qt.AlignTop)
        self.ui.search_verticallayout.setSpacing(10)
        
        # Set media type to index -1 (placeholder showing)
        self.ui.search_media_type.setCurrentIndex(-1)
        
        # Connect internal UI signals
        self.ui.search_line.returnPressed.connect(self._on_search_clicked)
        self.ui.serach_button.clicked.connect(self._on_search_clicked)
        self.ui.source.currentIndexChanged.connect(self._on_source_changed)
        self.ui.search_line.textChanged.connect(self._on_text_changed)
        
        # Initialize UI state
        self._on_source_changed(self.ui.source.currentIndex())
    
    def _on_source_changed(self, index):
        """Internal handler for source changes"""
        if index == 0:  # DB
            self.ui.serach_button.setVisible(False)
        elif index == 1:  # API
            self.ui.serach_button.setVisible(True)
        
        # Clear results and emit signal
        self.clear_results()
        self.source_changed.emit(index)
    
    def _on_text_changed(self, text):
        """Internal handler for text changes"""
        self.text_changed.emit(text)
    
    def _on_search_clicked(self):
        """Internal handler for search button/enter key"""
        # Validate media type
        if not self.validate_media_type():
            return
        
        query = self.ui.search_line.text().strip()
        media_type = self.ui.search_media_type.currentText()
        source = "db" if self.ui.source.currentIndex() == 0 else "api"
        
        if query:
            self.search_requested.emit(query, media_type, source)
    
    # Public methods for presenter to control the view
    def validate_media_type(self) -> bool:
        """Validate that a media type is selected"""
        if self.ui.search_media_type.currentIndex() == -1:
            QMessageBox.warning(
                self,
                "Media Type Required",
                "Please select a media type before searching."
            )
            return False
        return True
    
    def clear_results(self):
        """Remove all widgets from the results layout"""
        while self.ui.search_verticallayout.count():
            item = self.ui.search_verticallayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def add_search_result(self, card: MediaCard):
        """Add a card widget to the results"""
        self.ui.search_verticallayout.addWidget(card)
    
    def get_search_text(self) -> str:
        """Get current search text"""
        return self.ui.search_line.text().strip()
    
    def get_media_type(self) -> str:
        """Get selected media type"""
        return self.ui.search_media_type.currentText()
    
    def get_source_index(self) -> int:
        """Get selected source index"""
        return self.ui.source.currentIndex()
    
    def show_error(self, message: str):
        """Display error message"""
        QMessageBox.critical(self, "Error", message)
    
    def set_enabled(self, enabled: bool):
        """Enable/disable search controls"""
        self.ui.search_line.setEnabled(enabled)
        self.ui.serach_button.setEnabled(enabled)
        self.ui.search_media_type.setEnabled(enabled)
        self.ui.source.setEnabled(enabled)