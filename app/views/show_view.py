from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, Signal
from resources.py_ui.show_ui import Ui_show
from app.utils.image_loder import get_image_loader

class ShowView(QDialog):
    """Pure UI component for show dialog"""
    
    def __init__(self):
        super().__init__()
        # Setup UI
        self.ui = Ui_show()
        self.ui.setupUi(self)
        self.image_loader = get_image_loader()

    def set_detail_data(self, detail_data: dict):
        """Populate the dialog with detail data"""
        self.ui.title_lable.setText(detail_data.get("title", ""))
        self.ui.gener_lable.setText(detail_data.get("genres", ""))
        self.ui.released_lable.setText(detail_data.get("released", ""))
        self.ui.runtime__lable.setText(detail_data.get('runtime', ''))
        self.ui.tmdb_rating.setText(detail_data.get("tmdb_rating", ""))
        self.ui.tmdb_votes.setText(detail_data.get("tmdb_votes", ""))
        self.ui.imdb_rating.setText(detail_data.get("imdb_rating", ""))
        self.ui.imdb_votes.setText(detail_data.get("imdb_votes", ""))

        self.ui.user_rating.setText(detail_data.get("user_rating", ""))
        self.ui.rotten_tomatos_rating.setText(detail_data.get("rottentomatos_rating", ""))
        self.ui.metascore_rating.setText(detail_data.get("metascore_rating", ""))
        self.ui.director_name.setText(detail_data.get("director_name", ""))

        



