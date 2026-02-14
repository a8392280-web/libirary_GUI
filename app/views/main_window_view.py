# views/main_widget_view.py
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel
from resources.py_ui.main_ui import Ui_main_widget
from PySide6.QtWidgets import QListView


class MainWidgetView(QWidget):
    # Signals
    logout_requested = Signal()
    add_requested = Signal()
    show_user_media = Signal(str, str, bool)  # category, section, force
    random_media_requested = Signal(str, str)  # category, section
    near_bottom = Signal(str)  # list_name
    search_requested = Signal(str, str, str)  # category, section, text
    
    # Navigation signals
    show_home_requested = Signal()
    show_movies_requested = Signal()
    show_series_requested = Signal()
    show_games_requested = Signal()
    show_books_requested = Signal()
    show_comics_requested = Signal()
    show_setting_requested = Signal()

    def __init__(self):
        super().__init__()
        
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)
        self.threshold = 100  # Threshold in pixels to trigger loading more items
        
        self.movies_search_line = {
            "planned": self.ui.search_line_2,
            "in_progress": self.ui.search_line_1,
            "on_hold": self.ui.search_line_3,
            "dropped": self.ui.search_line_4,
            "completed": self.ui.search_line_5,
            "favorites": self.ui.search_line_6
        }
        
        self._setup_buttons()

        self.dumb_label = QLabel("Dumb Label for Testing", self)
        self.dumb_label.hide()

    def _setup_buttons(self):
        # Side buttons
        self.ui.show_home.clicked.connect(self.show_home_requested.emit)
        self.ui.show_movies.clicked.connect(self.show_movies_requested.emit)
        # self.ui.show_series.clicked.connect(self.show_series_requested.emit)
        # self.ui.show_anime.clicked.connect(self.show_anime_requested.emit)
        # self.ui.show_games.clicked.connect(self.show_games_requested.emit)
        # self.ui.show_books.clicked.connect(self.show_books_requested.emit)
        # self.ui.show_comics.clicked.connect(self.show_comics_requested.emit)
        self.ui.show_setting.clicked.connect(self.show_setting_requested.emit)

        self.ui.show_movies.clicked.connect(lambda: self.set_user_media("movies", "in_progress"))
        self.ui.tap_widget.currentChanged.connect(self.on_tab_changed)

        # Refresh buttons
        self.ui.refresh_button_1.clicked.connect(lambda: self.set_user_media("movies", "in_progress", True))
        self.ui.refresh_button_2.clicked.connect(lambda: self.set_user_media("movies", "planned", True))
        self.ui.refresh_button_3.clicked.connect(lambda: self.set_user_media("movies", "on_hold", True))
        self.ui.refresh_button_4.clicked.connect(lambda: self.set_user_media("movies", "dropped", True))
        self.ui.refresh_button_5.clicked.connect(lambda: self.set_user_media("movies", "completed", True))
        self.ui.refresh_button_6.clicked.connect(lambda: self.set_user_media("movies", "favorites", True))

        # Random buttons
        self.ui.random_button_1.clicked.connect(lambda: self.random_media_requested.emit("movie", "in_progress"))
        self.ui.random_button_2.clicked.connect(lambda: self.random_media_requested.emit("movie", "planned"))
        self.ui.random_button_3.clicked.connect(lambda: self.random_media_requested.emit("movie", "on_hold"))
        self.ui.random_button_4.clicked.connect(lambda: self.random_media_requested.emit("movie", "dropped"))
        self.ui.random_button_5.clicked.connect(lambda: self.random_media_requested.emit("movie", "completed"))
        self.ui.random_button_6.clicked.connect(lambda: self.random_media_requested.emit("movie", "favorites"))

        # Scroll detection
        self.ui.list_view_1.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("list_view_1"))
        self.ui.list_view_2.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("list_view_2"))
        self.ui.list_view_3.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("list_view_3"))
        self.ui.list_view_4.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("list_view_4"))
        self.ui.list_view_5.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("list_view_5"))
        self.ui.list_view_6.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("list_view_6"))

        # Search and logout
        self.ui.add_button.clicked.connect(self.add_requested.emit)
        self.ui.logout.clicked.connect(self.logout_requested.emit)

        # Hide search bars initially
        for section, line_edit in self.movies_search_line.items():
            line_edit.hide()
            line_edit.textChanged.connect(lambda text, s=section: self.search_requested.emit("movies", s, text))

        # Sort combo box
        self.ui.sort_button.addItems([
            "Title (A-Z)",
            "Title (Z-A)",
            "Released (Oldest)",
            "Released (Newest)"
        ])

    def set_user_media(self, category: str, section: str, force: bool = False):
        self.show_user_media.emit(category, section, force)

    def set_current_index(self, index: int):
        self.ui.stacked_body_Widget.setCurrentIndex(index)

    def set_logout_enabled(self, enabled: bool):
        self.ui.logout.setEnabled(enabled)

    def set_logout_text(self, text: str):
        self.ui.logout.setText(text)

    def on_tab_changed(self, index):
        """Called whenever user switches tabs"""
        # ✅ Use same mapping as presenter's SECTION_CONFIG
        section_map = {
            0: "in_progress",
            1: "planned",
            2: "on_hold",
            3: "dropped",
            4: "completed",
            5: "favorites"
        }
        
        if index in section_map:
            self.set_user_media("movies", section_map[index])

    def update_view_layout(self, target_view, mode: str):
        """Changes the QListView layout properties and resets them correctly."""
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

    def _check_scroll(self, list_name):
        list_widget = getattr(self.ui, list_name)
        scrollbar = list_widget.verticalScrollBar()
        
        if scrollbar.maximum() - scrollbar.value() < self.threshold:
            self.near_bottom.emit(list_name)


    def is_list_starving(self, list_name):
        """Returns True if the list content doesn't fill the viewable area."""
        list_widget = getattr(self.ui, list_name)
        scrollbar = list_widget.verticalScrollBar()
        
        # If maximum is 0, the content fits entirely inside the window (no scrolling)
        return scrollbar.maximum() <= 0