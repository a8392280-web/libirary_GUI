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
    async def show_detail_dialog(api, media_type: str, item_id: int):
        """
        Fetches data and opens a detail dialog for any media type.
        
        Args:
            api: APIClient instance
            media_type: 'movie', 'series', 'game', etc.
            item_id: The ID of the media item
            
        Returns:
            Dialog result code (QDialog.Accepted/Rejected) or None on error
        """
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        
        try:
            # Fetch data
            detail_data = await api.get(f"users/me/media/{media_type}/{item_id}")
            
            # Restore cursor as soon as data arrives
            QApplication.restoreOverrideCursor()
            
            if detail_data is None:
                QMessageBox.warning(
                    None, 
                    "Connection Issue", 
                    "Could not retrieve data from server."
                )
                return None
            
            # Setup View and Presenter
            show_dialog = ShowView()
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
            # Ensure cursor is restored even on error
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
        """
        Runs a dialog asynchronously with safety checks.
        
        Args:
            dialog: QDialog instance
            
        Returns:
            Dialog result code
        """
        future = asyncio.get_running_loop().create_future()
        
        # Success path: Dialog finishes normally
        def handle_finished(result):
            if not future.done():
                future.set_result(result)
        
        # Safety path: Dialog destroyed before finishing
        def handle_destroyed():
            if not future.done():
                future.set_result(0)  # QDialog.Rejected
        
        dialog.finished.connect(handle_finished)
        dialog.destroyed.connect(handle_destroyed)
        
        # Open as window-modal but non-blocking
        dialog.open()
        
        try:
            return await future
        finally:
            # Disconnect signals to prevent memory leaks
            try:
                dialog.finished.disconnect(handle_finished)
                dialog.destroyed.disconnect(handle_destroyed)
            except Exception:
                pass  # Dialog might already be gone