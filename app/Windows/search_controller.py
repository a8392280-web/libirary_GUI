import asyncio
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, QTimer
from resources.py_ui.search_ui import Ui_add_widget
from resources.py_ui.search_card_ui import MediaCard
from app.api.client import LibraryAPIClient

class AddWidgetController(QDialog):
    def __init__(self):
        super().__init__()
        # Setup UI
        self.ui = Ui_add_widget()
        self.ui.setupUi(self)
        self.client = LibraryAPIClient()
        
        # Set alignment and spacing
        self.ui.search_verticallayout.setAlignment(Qt.AlignTop)
        self.ui.search_verticallayout.setSpacing(10)
        
        # Set media type to index -1 (placeholder showing)
        self.ui.search_media_type.setCurrentIndex(-1)
        
        # Connect signals
        self.ui.search_line.returnPressed.connect(self.handle_search)
        self.ui.serach_button.clicked.connect(self.handle_search)
        
        # Connect source combo box
        self.ui.source.currentIndexChanged.connect(self.on_source_changed)
        
        # Debounce timer for automatic search (DB mode)
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.handle_search)
        self.ui.search_line.textChanged.connect(self.on_text_changed)
        
        # Track current search task
        self._current_task = None
        
        # Initialize UI state
        self.on_source_changed(self.ui.source.currentIndex())
    
    def on_source_changed(self, index):
        """Handle source combo box changes"""
        if index == 0:  # DB
            # Hide search button
            self.ui.serach_button.setVisible(False)
            # Clear results when switching to DB
            self.clear_results()
        elif index == 1:  # API
            # Show search button
            self.ui.serach_button.setVisible(True)
            # Clear results when switching to API
            self.clear_results()
    
    def on_text_changed(self, text):
        """Handle text changes - only auto-search in DB mode"""
        # Stop the timer if it's running
        self.search_timer.stop()
        
        # Only auto-search if source is DB (index 0)
        if self.ui.source.currentIndex() != 0:
            return
        
        if not self.ui.search_line.text().strip():
            # Clear results when search box is empty
            self.clear_results()
            # Cancel any ongoing search
            if self._current_task and not self._current_task.done():
                self._current_task.cancel()
            return
        
        # Start debounce timer (500ms) for DB mode
        self.search_timer.start(500)
    
    def clear_results(self):
        """Remove all widgets from the results layout"""
        while self.ui.search_verticallayout.count():
            item = self.ui.search_verticallayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def add_search_result(self, title, cover_url, description, released, item_id):
        """Creates and adds a new card to the UI"""
        card = MediaCard(title, cover_url, description, released, item_id)
        self.ui.search_verticallayout.addWidget(card)
    
    def validate_media_type(self):
        """Validate that a media type is selected"""
        if self.ui.search_media_type.currentIndex() == -1:
            QMessageBox.warning(
                self,
                "Media Type Required",
                "Please select a media type before searching."
            )
            return False
        return True
    
    def handle_search(self):
        """Non-async slot that schedules the async search"""
        # Validate media type first
        if not self.validate_media_type():
            return
        
        # Cancel previous search if still running
        if self._current_task and not self._current_task.done():
            self._current_task.cancel()
        
        # Schedule the async search
        self._current_task = asyncio.create_task(self._handle_search_async())
    
    async def _handle_search_async(self):
        """Actual async search implementation"""
        query = self.ui.search_line.text().strip()
        media_type = self.ui.search_media_type.currentText()
        source_index = self.ui.source.currentIndex()
        
        if not query:
            return
        
        try:
            # Clear old results
            self.clear_results()
            
            # Choose endpoint based on source
            if source_index == 0:  # DB
                print(f"Searching DB for '{query}' in {media_type}...")
                response = await self.client.get(f"media/movies/search/?q={query}")
            elif source_index == 1:  # API
                print(f"Fetching from API for '{query}' in {media_type}...")
                response = await self.client.get(f"media/movies/api-search/tmdb?title={query}")
            else:
                return
            
            # Handle response
            if response and isinstance(response, list):
                for result in response:
                    # Check if task was cancelled
                    if asyncio.current_task().cancelled():
                        break
                    
                    self.add_search_result(
                        title=result.get("title"),
                        cover_url=result.get("cover_url"),
                        description=result.get("description"),
                        released=result.get("released"),
                        item_id=result.get("id")
                    )
                    # Small delay to avoid blocking UI
                    await asyncio.sleep(0.01)
                    
        except asyncio.CancelledError:
            print("Search cancelled")
        except Exception as e:
            print(f"Search error: {e}")