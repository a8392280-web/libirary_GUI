# views/main_widget_view.py
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel
from resources.py_ui.main_ui import Ui_main_widget
from PySide6.QtCore import QTimer
from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QListView

class MainWidgetView(QWidget):
    # Signals
    logout_requested = Signal()
    search_requested = Signal()
    show_user_media = Signal(str, str, bool)  # category, section
    random_media_requested = Signal(str, str)  # category, section
    
    # Optional: navigation signals
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

        self.movies_search_line = {
                "planned": self.ui.movies_search_2,
                "in_progress": self.ui.movies_search_1,
                "on_hold": self.ui.movies_search_3,
                "dropped": self.ui.movies_search_4,
                "completed": self.ui.movies_search_5,
                "favorites": self.ui.movies_search_6
            }
        

        self._setup_buttons()

        self.dumb_label = QLabel("Dumb Label for Testing", self)
        self.dumb_label.hide()  # Hide it as it's only for image loading tests
        


    def _setup_buttons(self):
        # Side buttons
        self.ui.show_home.clicked.connect(lambda: self.show_home_requested.emit())
        self.ui.show_movies.clicked.connect(lambda: self.show_movies_requested.emit())
        self.ui.show_series.clicked.connect(lambda: self.show_series_requested.emit())
        self.ui.show_games.clicked.connect(lambda: self.show_games_requested.emit())
        self.ui.show_books.clicked.connect(lambda: self.show_books_requested.emit())
        self.ui.show_comics.clicked.connect(lambda: self.show_comics_requested.emit())
        self.ui.show_setting.clicked.connect(lambda: self.show_setting_requested.emit())

        self.ui.show_movies.clicked.connect(lambda: self.set_user_media("movies", "in_progress"))
        self.ui.movies_tap_widget.currentChanged.connect(self.on_tab_changed)


        self.ui.refresh_button_1.clicked.connect(lambda: self.set_user_media("movies", "in_progress",True))
        self.ui.refresh_button_2.clicked.connect(lambda: self.set_user_media("movies", "planned",True))
        self.ui.refresh_button_3.clicked.connect(lambda: self.set_user_media("movies", "on_hold",True))
        self.ui.refresh_button_4.clicked.connect(lambda: self.set_user_media("movies", "dropped",True))
        self.ui.refresh_button_5.clicked.connect(lambda: self.set_user_media("movies", "completed",True))
        self.ui.refresh_button_6.clicked.connect(lambda: self.set_user_media("movies", "favorites", True))


        self.ui.movies_random_button_1.clicked.connect(lambda: self.random_media_requested.emit("movie", "in_progress"))
        self.ui.movies_random_button_2.clicked.connect(lambda: self.random_media_requested.emit("movie", "planned"))
        self.ui.movies_random_button_3.clicked.connect(lambda: self.random_media_requested.emit("movie", "on_hold"))
        self.ui.movies_random_button_4.clicked.connect(lambda: self.random_media_requested.emit("movie", "dropped"))
        self.ui.movies_random_button_5.clicked.connect(lambda: self.random_media_requested.emit("movie", "completed"))
        self.ui.movies_random_button_6.clicked.connect(lambda: self.random_media_requested.emit("movie", "favorites"))


        # Search button
        self.ui.movies_add_botton.clicked.connect(lambda: self.search_requested.emit())

        # Logout button
        self.ui.logout.clicked.connect(lambda: self.logout_requested.emit())

        # hide search bars initially
        for line_edit in self.movies_search_line.values():
            line_edit.hide()

        self.ui.movies_sort_by.addItems([
                "Title (A-Z)",
                "Title (Z-A)",
                "Released (Oldest)",
                "Released (Newest)"
            ])

        

    def set_user_media(self, category: str, section: str, force: bool = False):
        print(f"Emitting show_user_media with category: {category}, section: {section}, force: {force}")
        self.show_user_media.emit(category, section, force)

    # Methods to update UI
    def set_current_index(self, index: int):
        self.ui.stacked_body_Widget.setCurrentIndex(index)

    def set_logout_enabled(self, enabled: bool):
        self.ui.logout.setEnabled(enabled)

    def set_logout_text(self, text: str):
        self.ui.logout.setText(text)

    def on_tab_changed(self, index):
        """Called whenever user switches tabs"""
        print(f"User switched to tab index: {index}")
        
        if index == 0:
            self.set_user_media("movies", "in_progress")
        elif index == 1:
            self.set_user_media("movies", "planned")
        elif index == 2:
           self.set_user_media("movies", "on_hold")
        elif index == 3:
           self.set_user_media("movies", "dropped")
        elif index == 4:
           self.set_user_media("movies", "completed")
        elif index == 5:
            self.set_user_media("movies", "favorites")


    # app/views/main_widget_view.py

    def update_view_layout(self, target_view, mode: str):
        """Changes the QListView layout properties and resets them correctly."""
        if mode == "grid":
            # Reset to Grid settings
            target_view.setViewMode(QListView.IconMode)
            target_view.setFlow(QListView.LeftToRight) # Essential for grid wrapping
            target_view.setResizeMode(QListView.Adjust)
            target_view.setMovement(QListView.Static)
            target_view.setWrapping(True)
            target_view.setSpacing(15) # Give cards some breathing room
        else:
            # Reset to List settings
            target_view.setViewMode(QListView.ListMode)
            target_view.setFlow(QListView.TopToBottom) # Essential for vertical list
            target_view.setResizeMode(QListView.Fixed)
            target_view.setWrapping(False)
            target_view.setSpacing(0)
        
        # Force the view to recalculate item positions immediately
        target_view.doItemsLayout()