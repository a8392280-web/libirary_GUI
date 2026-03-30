from PySide6.QtWidgets import QDialog, QMessageBox, QListView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from resources.py_ui.search_ui import Ui_add_widget
from app.views.media_delegate import MediaDelegate
from app.utils.loading_spinner import SpinnerOverlay


class SearchView(QDialog):
    """Pure UI component for search dialog"""
    
    # Signals for user actions
    search_requested = Signal(str, str)  # query, media_type
    source_changed = Signal(int)  # source index
    text_changed = Signal(str)  # search text
    
    def __init__(self):
        super().__init__()
        # Setup UI
        self.ui = Ui_add_widget()
        self.ui.setupUi(self)
        
        # Setup model and delegate
        self.results_model = QStandardItemModel()
        self.ui.search_listView.setModel(self.results_model)
        self.ui.search_listView.setItemDelegate(MediaDelegate())

        # Spinner overlay for loading state
        self._spinner = SpinnerOverlay(self.ui.search_listView)
        
        # Set media type to index -1 (placeholder showing)
        self.ui.search_media_type.setCurrentIndex(-1)
        
        # Connect internal UI signals
        self.ui.search_line.returnPressed.connect(self._on_search_clicked)
        self.ui.serach_button.clicked.connect(self._on_search_clicked)

    
    def _on_search_clicked(self):
        """Internal handler for search button/enter key"""

        # Validate media type
        if not self.validate_media_type():
            return
        
        query = self.ui.search_line.text().strip()
        media_type = self.ui.search_media_type.currentText()
        
        if query:
            self.search_requested.emit(query, media_type)
    

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
        """Clear all results from the list view"""
        self.results_model.clear()
    

    def add_search_result(self, result: dict):
        """Add a search result to the list view"""
        print(f"Adding search result to view: {result.get('cover_url')}")

        standard_item = QStandardItem()
        standard_item.setData(result.get("title"), Qt.UserRole + 1)
        standard_item.setData(result.get("released"), Qt.UserRole + 2)
        standard_item.setData(result.get("id"), Qt.UserRole + 4)
        cover_url = result.get("cover_url", "")
        standard_item.setData(cover_url, Qt.UserRole + 5)
        standard_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        
        # Store full result data for detail view
        standard_item.setData(result, Qt.UserRole + 10)
        
        self.results_model.appendRow(standard_item)
    
    def get_search_text(self) -> str:
        """Get current search text"""
        return self.ui.search_line.text().strip()
    
    def get_media_type(self) -> str:
        """Get selected media type"""
        return self.ui.search_media_type.currentText()
    

    def show_error(self, message: str):
        """Display error message"""
        QMessageBox.critical(self, "Error", message)
    
    def set_enabled(self, enabled: bool):
        """Enable/disable search controls"""
        self.ui.search_line.setEnabled(enabled)
        self.ui.serach_button.setEnabled(enabled)
        self.ui.search_media_type.setEnabled(enabled)

    def set_loading(self, loading: bool):
        """Show/hide loading spinner over results"""
        if loading:
            self._spinner.start()
        else:
            self._spinner.stop()
    
    def update_view_layout(self, mode: str):
        """Update search results between grid and list modes"""
        if mode == "grid":
            self.ui.search_listView.setViewMode(QListView.IconMode)
            self.ui.search_listView.setFlow(QListView.LeftToRight)
            self.ui.search_listView.setResizeMode(QListView.Adjust)
            self.ui.search_listView.setMovement(QListView.Static)
            self.ui.search_listView.setWrapping(True)
            self.ui.search_listView.setSpacing(15)
        else:  # list mode
            self.ui.search_listView.setViewMode(QListView.ListMode)
            self.ui.search_listView.setFlow(QListView.TopToBottom)
            self.ui.search_listView.setResizeMode(QListView.Fixed)
            self.ui.search_listView.setWrapping(False)
            self.ui.search_listView.setSpacing(0)
        self.ui.search_listView.doItemsLayout()
