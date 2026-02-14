import asyncio
import webbrowser
from PySide6.QtCore import QTimer
from qasync import asyncSlot
import httpx
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QWidget, QHBoxLayout, QLabel, QMessageBox
from PySide6.QtGui import QIcon, QFont, QColor, QPixmap
from PySide6.QtCore import Qt
from app.utils.movies_fetch import search_arabseed,search_akwam

class ShowPresenter:
    def __init__(self, view, api, media_type, media_data):
        self.view = view
        self.api = api
        self.media_type = media_type
        self.media_data = media_data
        
        # Single debounce timer for all updates
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        # asyncSlot is handled via the decorator on the method definition below
        self.update_timer.timeout.connect(self._update_media)
        
        # Store pending updates
        self.pending_updates = {}
        
        # Connect view signals
        self.view.category_changed.connect(self.on_category_changed)
        self.view.user_rating_changed.connect(self.on_user_rating_changed)
        self.view.favorite_toggled.connect(self.on_favorite_toggled)
        
        # Set the categories
        self.movies_catag = ["Planned", "In_progress", "Completed", "On_hold", "Dropped"]
        
        if media_type == "movie":
            self.view.set_category_options(self.movies_catag)
        
        self.view.set_details(self.prepare_movie_for_ui(media_data))

        self.setup_media_type_ui()

        self.view.ui.find_button_1.clicked.connect(self.on_find_button_1_clicked)
        self.view.ui.find_button_2.clicked.connect(self.on_find_button_2_clicked)
        self.view.ui.find_button_3.clicked.connect(self.on_find_button_3_clicked)
        self.view.ui.find_button_4.clicked.connect(self.on_find_button_4_clicked)



    def setup_media_type_ui(self):
        if self.media_type == "movie":
            self.view.ui.tabWidget.setTabVisible(2, False)

        self.view.ui.find_button_1.setText("Cineby")
        self.view.ui.find_button_2.setText("VidSrc")
        self.view.ui.find_button_3.setText("ArabSeed")
        self.view.ui.find_button_4.setText("Akwam")



    
    def prepare_movie_for_ui(self, movie: dict) -> dict:
        # ---------- Runtime ----------
        runtime = movie.get("media", {}).get("runtime", 0)
        if runtime:
            hours = runtime // 60
            minutes = runtime % 60
            movie["media"]["runtime"] = f"{hours}h {minutes}m"
        else:
            movie["media"]["runtime"] = "N/A"
        
        # ---------- Director ----------
        if movie.get("media", {}).get("director"):
            parts = movie["media"]["director"].split(",", 1)
            director_name = parts[0].strip()
            director_image = ""
            if len(parts) > 1:
                director_image = parts[1].strip()
            movie["media"]["director_name"] = director_name
            movie["media"]["director_image"] = director_image
        
        # ---------- Genres ----------
        movie["media"]["genres"] = ", ".join(movie.get("media", {}).get("genres", []))
        return movie
    
    def on_category_changed(self, new_category: str):
        """Called when user changes category"""
        print(f"User selected category: {new_category}")
        self.pending_updates["status"] = new_category.lower()
        self.update_timer.start(3000) 
    
    def on_user_rating_changed(self, new_rating: float):
        """Called when user changes rating"""
        print(f"User updated rating to: {new_rating}")
        self.pending_updates["user_rating"] = new_rating
        self.update_timer.start(3000)

    def on_favorite_toggled(self, is_favorite: bool):
        """Called when user toggles favorite status"""
        print(f"User toggled favorite to: {is_favorite}")
        self.pending_updates["favorite"] = is_favorite
        self.update_timer.start(3000)


    @asyncSlot() # <--- CRITICAL: Allows QTimer to trigger this async function
    async def _update_media(self):
        if not self.pending_updates:
            return
        
        # Make a copy and clear immediately
        updates = self.pending_updates.copy()
        self.pending_updates.clear()
        
        print(f"Updating media with: {updates}")
        
        try:
            media_id = self.media_data.get("media", {}).get("id")

            response = await self.api.post(
                f"users/me/media/save?media_id={media_id}&media_type={self.media_type}", 
                json=updates
            )

            print(f"Response: {response}")
            print("Media updated successfully!")
            
        except Exception as e:
            print(f"Error updating media: {e}")
            import traceback
            traceback.print_exc()
            
            # Optional: Put updates back into pending if network failed
            # self.pending_updates.update(updates)

    @asyncSlot()
    async def cleanup(self):
        """Force save any pending updates when dialog closes"""
        if self.pending_updates:
            print("Dialog closing, forcing save of pending updates...")
            self.update_timer.stop()
            await self._update_media()


    def on_find_button_1_clicked(self):
        print("Button clicked")
        tmdb_id = self.media_data.get("media",{}).get("tmdb_id",None)
        if tmdb_id:
            url = f"https://www.vidking.net/embed/{self.media_type}/{tmdb_id}"
            webbrowser.open(url)
            print(f"Opened: {url}")

    def on_find_button_2_clicked(self):
        print("Button clicked")
        tmdb_id = self.media_data.get("media",{}).get("tmdb_id",None)
        if tmdb_id:
            url = f"https://vidsrc-embed.ru/embed/{self.media_type}?tmdb={tmdb_id}"
            webbrowser.open(url)
            print(f"Opened: {url}")

    def on_find_button_3_clicked(self):
        print("Button clicked")
        asyncio.create_task(self.arabseed_search())


    async def arabseed_search(self):
        button = self.view.ui.find_button_3

        self.view.ui.find_button_3.setEnabled(False)
        self.view.ui.find_button_4.setEnabled(False)

        # change UI state
        button.setEnabled(False)
        button.setText("Searching...")


        try:
            title = self.media_data.get("media", {}).get("title")

            if not title:
                print("No title found")
                return

            title = title.replace(":", " ")

            url = await search_arabseed(title)

            if url:
                webbrowser.open(url)
                print(f"Opened: {url}")

            else:
                QMessageBox.information(
                    self.view,
                    "Not Found",
                    "No result found on ArabSeed."
                )
                print("No result found")

        finally:
            # ALWAYS restore button even if error happens
            button.setEnabled(True)
            button.setText("ArabSeed")
            self.view.ui.find_button_3.setEnabled(True)
            self.view.ui.find_button_4.setEnabled(True)



    def on_find_button_4_clicked(self):
        print("Button clicked")
        asyncio.create_task(self.akwam_search())


    async def akwam_search(self):
        button = self.view.ui.find_button_4

        self.view.ui.find_button_3.setEnabled(False)
        self.view.ui.find_button_4.setEnabled(False)

        # change UI state
        button.setEnabled(False)
        button.setText("Searching...")


        try:
            title = self.media_data.get("media", {}).get("title")
            year = self.media_data.get("media", {}).get("released")

            if not title:
                print("No title found")
                return

            title = title.replace(":", "")

            url = await search_akwam(title,year if year else 0)

            if url:
                webbrowser.open(url)
                print(f"Opened: {url}")

            else:
                QMessageBox.information(
                    self.view,
                    "Not Found",
                    "No result found on Akwam."
                )
                print("No result found")

        finally:
            # ALWAYS restore button even if error happens
            button.setEnabled(True)
            button.setText("Akwam")
            self.view.ui.find_button_3.setEnabled(True)
            self.view.ui.find_button_4.setEnabled(True)

