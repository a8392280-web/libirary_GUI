from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, Signal, QEvent
from app.views.cast_view import CastCard
from resources.py_ui.show_ui import Ui_show
from app.utils.image_loder import get_image_loader
import webbrowser
from .user_rating_view import UserRatingView

class ShowView(QDialog):
    """Pure UI component for show dialog"""
    category_changed = Signal(str)
    user_rating_changed = Signal(float)
    favorite_toggled = Signal(bool)
    
      

    def __init__(self):
        super().__init__()
        # Setup UI
        self.ui = Ui_show()
        self.ui.setupUi(self)
        self.image_loader = get_image_loader()
        self.id = None

        self.ui.status_combobox.currentTextChanged.connect(self.category_changed.emit) # Emit signal on category change
        self.ui.description_Button.clicked.connect(self._on_description_clicked) # Show description
        self.ui.trailer_Button.clicked.connect(self._on_trailer_clicked) # Open trailer link
        self.ui.favorite_button.toggled.connect(self.on_favorite_toggled) # Emit signal on favorite toggle

        # Install event filter to detect clicks on user_rating_widget
        self.ui.user_rating_widget.installEventFilter(self)
        # Make it look clickable
        self.ui.user_rating_widget.setCursor(Qt.PointingHandCursor)

    def eventFilter(self, obj, event):
        """Catch clicks on user_rating_widget"""
        if obj == self.ui.user_rating_widget and event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self._on_rating_widget_clicked()
                return True
        return super().eventFilter(obj, event)
    

    def _on_rating_widget_clicked(self):
        current_rating = float(self.ui.user_rating.text()) if self.ui.user_rating.text() in  ["User rate", None] else 0.0
        rating_dialog = UserRatingView(current_rating, self)
        rating_dialog.rating_changed.connect(self._on_rating_updated)
        rating_dialog.exec()

    def _on_rating_updated(self, new_rating):
        """Handle the new rating"""
        print(f"New rating: {new_rating}")
        self.ui.user_rating.setText(f"{float(new_rating)}")

        # Save to database/emit to presenter
        self.user_rating_changed.emit(float(new_rating))

    def on_favorite_toggled(self, checked):
        print(f"Favorite toggled: {checked}")
        self.favorite_toggled.emit(checked) 


    def set_details(self, details: dict):
        media_details = details.get("media", {})
        user_media_details = details.get("user_media", None)

        if media_details:
            self.ui.title_lable.setText(media_details.get("title", ""))
            self.ui.released_lable.setText(str(media_details.get("released", "")))
            self.ui.runtime__lable.setText(str(media_details.get("runtime", "")))
            self.ui.gener_lable.setText(str(media_details.get("genres", "")))
            self.image_loader.load_image(url=media_details.get("cover_url"),label=self.ui.cover_lable,width=180,height=270,placeholder="⏳",error_text="🖼️")
            self.ui.director_name.setText(media_details.get("director_name", ""))
            self.image_loader.load_image(url=media_details.get("director_image"),label=self.ui.director_cover_label,width=180,height=270,placeholder="⏳",error_text="🖼️")

            self.description = media_details.get("description", "")
            self.trailer_url = media_details.get("trailer", "")

            self.ui.tmdb_rating.setText(str(media_details.get("tmdb_rating", "")))
            self.ui.tmdb_votes.setText(str(media_details.get("tmdb_votes", "")))
            self.ui.imdb_rating.setText(str(media_details.get("imdb_rating", "")))
            self.ui.imdb_votes.setText(str(media_details.get("imdb_votes", "")))

            self.ui.rotten_tomatos_rating.setText(str(media_details.get("rotten_tomatoes", "")))
            self.ui.metascore_rating.setText(str(media_details.get("metascore", "")))
            self.cast = media_details.get("cast", [])
            self._show_cast()

            self.id = media_details.get("id", None)

        if user_media_details:
            self.ui.user_rating.setText(str(user_media_details.get("user_rating", "")))

            self.set_favorite_button(user_media_details.get("favorite", False))
            self.set_current_category(user_media_details.get("status", ""))


            # self.ui.user_review.setText(str(user_media_details.get("review", "")))
            # self.ui.user_notes.setText(str(user_media_details.get("notes", "")))
            # self.ui.user_progress.setValue(user_media_details.get("progress", 0))
            # self.ui.user_total_progress.setValue(user_media_details.get("total_progress", 0))




    def _on_description_clicked(self):
        QMessageBox.information(self, "Description", self.description)

    def _on_trailer_clicked(self):

        if self.trailer_url:
            webbrowser.open(self.trailer_url)
        else:
            QMessageBox.warning(self, "No Trailer", "Trailer URL is not available.")

    def _show_cast(self):
        
        for actor in self.cast:
            card = CastCard(
                name=actor.get("name", ""),
                character=actor.get("character", ""),
                profile_url=actor.get("profile", ""),
                load_image_func=self.image_loader.load_image
            )
            self.ui.cast_layout.addWidget(card)


    # Presenter calls this to populate options
    def set_category_options(self, categories: list[str]):
        self.ui.status_combobox.clear()
        self.ui.status_combobox.addItems(categories)

    # allow presenter to set current value
    def set_current_category(self, category: str):
        print(f"Setting current category to: {category}")
        
        if category:
            print(f"Finding index for category: {category}")
            index = self.ui.status_combobox.findText(category, Qt.MatchFixedString) # Case-insensitive
            print(f"Index found: {index}")
            if index >= 0:
                # 1. Block signals so currentTextChanged doesn't fire
                self.ui.status_combobox.blockSignals(True)
                
                print(f"Setting combobox index to: {index}")
                self.ui.status_combobox.setCurrentIndex(index)

                # 3. Unblock signals so the user can still trigger it manually later
                self.ui.status_combobox.blockSignals(False)

    def set_favorite_button(self, is_favorite: bool):
        self.ui.favorite_button.blockSignals(True)
        self.ui.favorite_button.setChecked(is_favorite)
        self.ui.favorite_button.blockSignals(False)