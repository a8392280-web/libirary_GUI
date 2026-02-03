import asyncio
from PySide6.QtCore import QTimer
from qasync import asyncSlot
import httpx

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
        
        # Set the categories
        self.movies_catag = ["Planned", "In_progress", "Completed", "On_hold", "Dropped"]
        
        if media_type == "movie":
            self.view.set_category_options(self.movies_catag)
        
        self.view.set_details(self.prepare_movie_for_ui(media_data))
    
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