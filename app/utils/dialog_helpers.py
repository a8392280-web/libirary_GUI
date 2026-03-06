# app/utils/dialog_helpers.py
import asyncio
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from app.views.show_view import ShowView
from app.presenters.show_presenter import ShowPresenter


class DialogHelper:
    """Reusable utilities for showing dialogs asynchronously"""
    
    @staticmethod
    async def show_detail_dialog(api, media_type: str, item_id: int = None, tmdb_id: int = None, 
                                 mal_id: int = None, rawg_id: int = None, ol_id: str = None):
        """
        Fetches data (DB or API) and opens a detail dialog for any media type.
        """
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        
        # ✅ Map plural/internal names to the singular form the backend expects
        MEDIA_MAP = {
            "movies": "movies",
            "movie": "movies",
            "series": "series",
            "games": "games",
            "game": "games",
            "anime": "anime",
            "books": "books",
            "book": "books",
            "manga": "manga",
            "comics": "manga" # If you use 'comics' in UI but 'manga' in backend
        }

        # Normalize the media_type (e.g., "movies" -> "movie")
        media_type = MEDIA_MAP.get(media_type.lower(), media_type)

        try:
            detail_data = None

            # 1. If we have an item_id, we are fetching from the user's personal collection
            if item_id:
                # Note: Fixed the URL structure to match standard REST patterns
                detail_data = await api.get(f"users/me/media/{media_type}/{item_id}")
                print(f"Fetched collection detail for {media_type}: {item_id}")

            # 2. If we have an external ID, we are fetching from the global API (TMDB, RAWG, etc.)
            elif tmdb_id:
                response = await api.post(f"media/{media_type}/from-api?tmdb_id={tmdb_id}")
                detail_data = {"user_media": None, "media": response}
            elif mal_id:
                response = await api.post(f"media/{media_type}/from-api?mal_id={mal_id}")
                detail_data = {"user_media": None, "media": response}
            elif rawg_id:
                response = await api.post(f"media/{media_type}/from-api?rawg_id={rawg_id}")
                detail_data = {"user_media": None, "media": response}
            elif ol_id:
                response = await api.post(f"media/{media_type}/from-api?ol_id={ol_id}")
                detail_data = {"user_media": None, "media": response}

            if not detail_data:
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(None, "Data Error", f"Could not retrieve details for this {media_type}.")
                return None

            # Restore cursor as soon as data arrives
            QApplication.restoreOverrideCursor()

            # Setup View and Presenter
            show_dialog = ShowView()
            # Pass normalized media_type so the presenter knows if it's a 'game', 'movie', etc.
            show_presenter = ShowPresenter(show_dialog, api, media_type, detail_data)
            
            # Prevent garbage collection
            show_dialog._presenter = show_presenter
            
            # Run dialog asynchronously
            result = await DialogHelper._wait_for_dialog(show_dialog)
            
            # Cleanup
            await show_presenter.cleanup()
            show_dialog.deleteLater()
            
            return result
            
        except Exception as e:
            QApplication.restoreOverrideCursor()
            print(f"Error loading detail: {e}")
            import traceback
            traceback.print_exc()
            
            QMessageBox.critical(
                None, 
                "Error", 
                f"An unexpected error occurred: {str(e)}"
            )
            return None
    
    @staticmethod
    async def _wait_for_dialog(dialog):
        """Runs a dialog asynchronously without blocking the event loop."""
        future = asyncio.get_running_loop().create_future()
        
        def handle_finished(result):
            if not future.done():
                future.set_result(result)
        
        def handle_destroyed():
            if not future.done():
                future.set_result(0) 
        
        dialog.finished.connect(handle_finished)
        dialog.destroyed.connect(handle_destroyed)
        
        dialog.open()
        
        try:
            return await future
        finally:
            try:
                dialog.finished.disconnect(handle_finished)
                dialog.destroyed.disconnect(handle_destroyed)
            except Exception:
                pass