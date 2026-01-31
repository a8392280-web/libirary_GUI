# views/main_widget_view.py
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel
from resources.py_ui.main_ui import Ui_main_widget

class MainWidgetView(QWidget):
    # Signals
    logout_requested = Signal()
    search_requested = Signal()
    show_user_media = Signal(str, str)  # category, section
    
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


        self.ui.show_setting.clicked.connect(lambda: self.show_setting_requested.emit())

        # Search button
        self.ui.movies_add_botton.clicked.connect(lambda: self.search_requested.emit())

        # Logout button
        self.ui.logout.clicked.connect(lambda: self.logout_requested.emit())

    def set_user_media(self, category: str, section: str):
        print(f"Emitting show_user_media with category: {category}, section: {section}")
        self.show_user_media.emit(category, section)

    # Methods to update UI
    def set_current_index(self, index: int):
        self.ui.stacked_body_Widget.setCurrentIndex(index)

    def set_logout_enabled(self, enabled: bool):
        self.ui.logout.setEnabled(enabled)

    def set_logout_text(self, text: str):
        self.ui.logout.setText(text)

    

