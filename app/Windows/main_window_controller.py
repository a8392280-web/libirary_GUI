# main_widget.py
from PySide6.QtCore import Qt, QSettings, Signal
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from resources.py_ui.main_ui import Ui_main_widget
from app.utils.refresh_token_strore import delete_refresh_token
from qasync import asyncSlot
from app.Windows.search_controller import AddWidgetController

class Widget(QWidget):
    logout_requested = Signal()
    
    def __init__(self, api_client):
        super().__init__()
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)
        self.setWindowTitle("My Library")
        self.api = api_client
        self.settings = QSettings("MyCompany", "MyApp")
        self._setup_side_buttons()
    
    def _setup_side_buttons(self):
        buttons = [
            ("show_home", self.show_home, "0"),
            ("show_movies", self.show_movies, "1"),
            ("show_series", self.show_series, "2"),
            ("show_games", self.show_games, "3"),
            ("show_books", self.show_books, "4"),
            ("show_comics", self.show_comics, "5"),
            ("show_setting", self.show_setting, "6"),
        ]
        for name, func, shortcut in buttons:
            btn = getattr(self.ui, name)
            btn.clicked.connect(func)
            btn.setShortcut(shortcut)
        
        # Add buttons
        self.ui.movies_add_botton.clicked.connect(self.open_add_movie_window)
        self.ui.movies_add_botton.setShortcut("+")
        
        # Logout button
        self.ui.logout.clicked.connect(self.handle_logout)
    
    def show_home(self):   
        self.ui.stacked_body_Widget.setCurrentIndex(0)
    
    def show_movies(self): 
        self.ui.stacked_body_Widget.setCurrentIndex(1)
    
    def show_series(self): 
        self.ui.stacked_body_Widget.setCurrentIndex(2)
    
    def show_games(self):  
        self.ui.stacked_body_Widget.setCurrentIndex(3)
    
    def show_books(self):  
        self.ui.stacked_body_Widget.setCurrentIndex(4)
    
    def show_comics(self): 
        self.ui.stacked_body_Widget.setCurrentIndex(5)
    
    def show_setting(self): 
        self.ui.stacked_body_Widget.setCurrentIndex(6)
    
    def open_add_movie_window(self):
        win = AddWidgetController()
        win.exec()
    
    @asyncSlot()
    async def handle_logout(self):
        """Handle logout with async API call"""
        # Confirm with the user
        reply = QMessageBox.question(
            self, 
            'Logout', 
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Disable logout button to prevent double-clicks
            self.ui.logout.setEnabled(False)
            self.ui.logout.setText("Logging out...")
            
            try:
                # Call the async API to clean up
                success = await self.api.logout()
                
                if success:
                    # Tell the controller we are done
                    self.logout_requested.emit()
                else:
                    # If server logout failed, still emit signal
                    # (local cleanup was done anyway)
                    QMessageBox.warning(
                        self, 
                        "Warning", 
                        "Server logout failed, but local session was cleared."
                    )
                    self.logout_requested.emit()
            
            except Exception as e:
                # If any error occurs, still allow logout locally
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Logout error: {e}\nLocal session will be cleared."
                )
                self.logout_requested.emit()
            
            finally:
                # Re-enable button (though window will close anyway)
                self.ui.logout.setEnabled(True)
                self.ui.logout.setText("Logout")