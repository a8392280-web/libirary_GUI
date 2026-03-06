# views/main_widget_view.py
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QListView
from resources.py_ui.main_ui import Ui_main_widget

class MainWidgetView(QWidget):
    # Signals
    logout_requested = Signal()
    add_requested = Signal()
    show_user_media = Signal(str, str, bool)  # category, section, force
    random_media_requested = Signal(str, str)  # category, section
    near_bottom = Signal(str)  # list_name
    search_requested = Signal(str, str, str)  # category, section, text
    clear_all_data_requested = Signal()
    
    # Navigation signals
    show_home_requested = Signal()
    show_setting_requested = Signal()

    def __init__(self):
        super().__init__()
        
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)
        
        # ✅ State Tracking
        self.current_category = "movies"  # Default starting category
        self.threshold = 100  # Pixels from bottom to trigger pagination
        
        # ✅ Dynamic Search Bar Mapping (Mapping UI elements to backend keys)
        self.search_lines = {
            "in_progress": self.ui.search_line_1,
            "planned":     self.ui.search_line_2,
            "on_hold":     self.ui.search_line_3,
            "dropped":     self.ui.search_line_4,
            "completed":   self.ui.search_line_5,
            "favorites":   self.ui.search_line_6
        }
        
        self._setup_connections()
        self._init_ui_states()

    def _init_ui_states(self):
        """Initial UI configuration"""
        # Hide search bars initially
        for line_edit in self.search_lines.values():
            line_edit.hide()

        # Initialize Sort Options
        self.ui.sort_button.addItems([
            "Title (A-Z)",
            "Title (Z-A)",
            "Released (Oldest)",
            "Released (Newest)"
        ])

    def _setup_connections(self):
        """Setup all button and signal connections"""
        
        # 1. Sidebar Navigation - Categories
        self.ui.show_movies.clicked.connect(lambda: self.set_active_category("movies"))
        self.ui.show_series.clicked.connect(lambda: self.set_active_category("series"))
        self.ui.show_games.clicked.connect(lambda: self.set_active_category("games"))
        self.ui.show_books.clicked.connect(lambda: self.set_active_category("books"))
        self.ui.show_comics.clicked.connect(lambda: self.set_active_category("manga"))
        self.ui.show_anime.clicked.connect(lambda: self.set_active_category("anime"))

        # 2. Sidebar Navigation - General
        self.ui.show_home.clicked.connect(self.show_home_requested.emit)
        self.ui.show_setting.clicked.connect(self.show_setting_requested.emit)
        self.ui.logout.clicked.connect(self.logout_requested.emit)
        

        # 3. Tab Navigation
        self.ui.tap_widget.currentChanged.connect(self.on_tab_changed)

        # 4. Action Buttons (Dynamic based on self.current_category)
        self.ui.add_button.clicked.connect(self.add_requested.emit)

        # Refresh Buttons (1-6)
        refresh_mapping = [
            (self.ui.refresh_button_1, "in_progress"),
            (self.ui.refresh_button_2, "planned"),
            (self.ui.refresh_button_3, "on_hold"),
            (self.ui.refresh_button_4, "dropped"),
            (self.ui.refresh_button_5, "completed"),
            (self.ui.refresh_button_6, "favorites"),
        ]
        for btn, section in refresh_mapping:
            btn.clicked.connect(lambda checked=False, s=section: self.set_user_media(self.current_category, s, True))

        # Random Buttons (1-6)
        random_mapping = [
            (self.ui.random_button_1, "in_progress"),
            (self.ui.random_button_2, "planned"),
            (self.ui.random_button_3, "on_hold"),
            (self.ui.random_button_4, "dropped"),
            (self.ui.random_button_5, "completed"),
            (self.ui.random_button_6, "favorites"),
        ]
        for btn, section in random_mapping:
            btn.clicked.connect(lambda checked=False, s=section: self.random_media_requested.emit(self.current_category, s))

        # 5. Search Line Edits
        for section, line_edit in self.search_lines.items():
            line_edit.textChanged.connect(lambda text, s=section: self.search_requested.emit(self.current_category, s, text))

        # 6. Scroll Detection (List views 1-6)
        for i in range(1, 7):
            list_view = getattr(self.ui, f"list_view_{i}")
            list_view.verticalScrollBar().valueChanged.connect(lambda val, n=f"list_view_{i}": self._check_scroll(n))

    # --- Logic Methods ---

    def set_active_category(self, category: str):
        """Changes the current category context and triggers a data reload."""
        self.current_category = category
        
        # Update the UI Label to match (Movies, Series, etc.)
        self.ui.title_label.setText(category.capitalize())
        
        # Switch the main stacked widget to the media view (assuming index 1)
        self.set_current_index(1)
        
        # Force reload for the current active tab
        current_tab_idx = self.ui.tap_widget.currentIndex()
        section = self.get_section_name_by_index(current_tab_idx)
        self.set_user_media(self.current_category, section, force=True)

        # Clear all data
        self.clear_all_data_requested.emit()


    def on_tab_changed(self, index: int):
        """Triggered when user clicks a different tab (e.g., 'Planned')"""
        section = self.get_section_name_by_index(index)
        if section:
            self.set_user_media(self.current_category, section)

    def get_section_name_by_index(self, index: int) -> str:
        """Helper to map tab index to section string"""
        mapping = {0: "in_progress", 1: "planned", 2: "on_hold", 3: "dropped", 4: "completed", 5: "favorites"}
        return mapping.get(index, "in_progress")

    def set_user_media(self, category: str, section: str, force: bool = False):
        """Emits signal to presenter to fetch data"""
        self.show_user_media.emit(category, section, force)

    def set_current_index(self, index: int):
        """Switch between Welcome (0), Library (1), or Settings (2)"""
        self.ui.stacked_body_Widget.setCurrentIndex(index)

    def set_logout_enabled(self, enabled: bool):
        self.ui.logout.setEnabled(enabled)

    def set_logout_text(self, text: str):
        self.ui.logout.setText(text)

    def update_view_layout(self, target_view, mode: str):
        """Adjusts the QListView between Grid and List modes"""
        if mode == "grid":
            target_view.setViewMode(QListView.IconMode)
            target_view.setFlow(QListView.LeftToRight)
            target_view.setResizeMode(QListView.Adjust)
            target_view.setMovement(QListView.Static)
            target_view.setWrapping(True)
            target_view.setSpacing(15)
        else:
            target_view.setViewMode(QListView.ListMode)
            target_view.setFlow(QListView.TopToBottom)
            target_view.setResizeMode(QListView.Fixed)
            target_view.setWrapping(False)
            target_view.setSpacing(0)
        
        target_view.doItemsLayout()

    def _check_scroll(self, list_name: str):
        """Detects if we are near the bottom of a list to trigger pagination"""
        list_widget = getattr(self.ui, list_name)
        scrollbar = list_widget.verticalScrollBar()
        if scrollbar.maximum() - scrollbar.value() < self.threshold:
            self.near_bottom.emit(list_name)

    def is_list_starving(self, list_name: str) -> bool:
        """Returns True if the list content doesn't fill the viewable area"""
        list_widget = getattr(self.ui, list_name)
        scrollbar = list_widget.verticalScrollBar()
        return scrollbar.maximum() <= 0