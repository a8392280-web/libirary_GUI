# presenters/main_widget_presenter.py
from app.utils.image_loder import get_image_loader
from app.views.movie_delegate import MovieDelegate
from app.views.search_view import SearchView
from app.presenters.search_presenter import SearchPresenter
from PySide6.QtWidgets import QMessageBox, QListView, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QCursor
from qasync import asyncSlot
import asyncio
from app.views.show_view import ShowView
from app.presenters.show_presenter import ShowPresenter



class MainWidgetPresenter:
    def __init__(self, view, api):
        self.view = view
        self.api = api
        self.movie_model = QStandardItemModel()
        self.delegate = MovieDelegate()
        self.search_dialog = None
        self.search_presenter = None

        # Connect View signals to presenter methods
        self.view.logout_requested.connect(self.handle_logout)
        self.view.search_requested.connect(self.show_search_dialog)
        self.view.show_user_media.connect(self.handle_show_user_media)

        self.view.show_home_requested.connect(lambda: self.view.set_current_index(0))
        self.view.show_movies_requested.connect(lambda: self.view.set_current_index(1))
        self.view.show_series_requested.connect(lambda: self.view.set_current_index(2))
        self.view.show_games_requested.connect(lambda: self.view.set_current_index(3))
        self.view.show_books_requested.connect(lambda: self.view.set_current_index(4))
        self.view.show_comics_requested.connect(lambda: self.view.set_current_index(5))
        self.view.show_setting_requested.connect(lambda: self.view.set_current_index(6))

    @asyncSlot()
    async def handle_logout(self):
        reply = QMessageBox.question(
            self.view,
            'Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.view.set_logout_enabled(False)
            self.view.set_logout_text("Logging out...")

            try:
                success = await self.api.logout()
                if not success:
                    QMessageBox.warning(
                        self.view,
                        "Warning",
                        "Server logout failed, but local session was cleared."
                    )
                # emit any global signal or perform navigation after logout
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    f"Logout error: {e}\nLocal session will be cleared."
                )
            finally:
                self.view.set_logout_enabled(True)
                self.view.set_logout_text("Logout")


    def show_search_dialog(self):
        self.search_dialog = SearchView()
        self.search_presenter = SearchPresenter(self.search_dialog, self.api)
        self.search_dialog.exec()
        if self.search_presenter:
            self.search_presenter.cleanup()
            self.search_presenter = None


    def get_category_lists(self, category: str):
    
        ui = self.view.ui
    
        category_widgets = {
            "movies": [ui.movies_list_1, ui.movies_list_2, ui.movies_list_3, ui.movies_list_4, ui.movies_list_5]
        }
        
        widgets = category_widgets[category]
        return {
            "in_progress": widgets[0],
            "planned":     widgets[1],
            "on_hold":     widgets[2],
            "dropped":     widgets[3],
            "completed":   widgets[4],
    }
    
        # In your presenter


    def handle_show_user_media(self, category: str, section: str):
        """Wrapper to call async load_section from signal"""
        asyncio.create_task(self.load_section(category, section))

    async def load_section(self, category: str, section: str):
        # 1. Fetch data
        data = await self.api.get(f"users/me/media/?media_type=movie&status={section}")
        
        target_view = self.get_category_lists(category)[section] # This is now a QListView
        
        # 2. Setup the View
        target_view.setItemDelegate(self.delegate)
        target_view.setModel(self.movie_model)
        target_view.setViewMode(QListView.IconMode)
        target_view.setResizeMode(QListView.Adjust)
        target_view.setSpacing(10)
        # In your Presenter or View
        target_view.setMovement(QListView.Static)  # Prevents users from dragging posters around
        target_view.setDragEnabled(False)          # Disables dragging out
        target_view.setAcceptDrops(False)         # Disables dropping into
        target_view.setEditTriggers(QListView.NoEditTriggers) # Prevents "Double-click to rename"
        
        

        # Connect the click signal
        target_view.clicked.connect(self.handle_item_click)

        # 3. Fill the Model
        self.movie_model.clear()
        for item in data:
            media = item.get("media", {})
            user_media = item.get("user_media", {})
            
            poster_url = media.get("cover_url", "")
            
            # Preload image into cache
            loader = get_image_loader()

            loader.load_image(
                poster_url,
                self.view.dumb_label,  # QLabel or hidden one
                140,
                190
            )

            standard_item = QStandardItem()
            # Store data in roles for the delegate to find
            standard_item.setData(media.get("title"), Qt.UserRole + 1)
            standard_item.setData(media.get("released"), Qt.UserRole + 2)
            standard_item.setData(media.get("id"), Qt.UserRole + 4) # ID
            standard_item.setData(media.get("cover_url"), Qt.UserRole + 5) # cover URL
            
            # Note: For images, you'll need a mechanism to load them into 
            # pixmaps and update the model item's Qt.UserRole + 3
            standard_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.movie_model.appendRow(standard_item)


    def handle_item_click(self, index):
        item_id = index.data(Qt.UserRole + 4)

        if item_id:
            print(f"Clicked item ID: {item_id}")
            asyncio.create_task(self._show_detail(item_id))
            
    async def _show_detail(self, item_id):
        """Fetches data and opens the detail dialog"""
        # 1. Show 'Busy' cursor so the user knows something is happening
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))       

        try:
            # 2. Fetch data (APIClient now handles retries internally)
            detail_data = await self.api.get(f"users/me/media/movie/{item_id}")
            
            # Restore normal cursor as soon as the data arrives
            QApplication.restoreOverrideCursor()

            if detail_data is None:
                # This happens if the APIClient returned None due to a refresh failure 
                # or a persistent network error after retries.
                QMessageBox.warning(None, "Connection Issue", "Could not retrieve data from server.")
                return

            # 3. Setup View and Presenter
            show_dialog = ShowView()
            show_presenter = ShowPresenter(show_dialog, self.api, "movie", detail_data)
            
            # Prevent Garbage Collection
            show_dialog._presenter = show_presenter 

            # 4. Run Dialog Asynchronously
            result = await self._wait_for_dialog(show_dialog)
            
            # 5. Cleanup
            await show_presenter.cleanup()
            show_dialog.deleteLater()
            
            return result
        
        except Exception as e:
            # Ensure cursor is restored even if an error occurs
            QApplication.restoreOverrideCursor()

        print(f"Error loading detail: {e}")
        import traceback
        traceback.print_exc()
        
        QMessageBox.critical(None, "Error", f"An unexpected error occurred: {str(e)}")

    def cancel_current_search(self):
        if self._current_task and not self._current_task.done():
            self._current_task.cancel()

    def cleanup(self):
        self.cancel_current_search()
        self.search_timer.stop()



    async def _wait_for_dialog(self, dialog):
        """
        Runs a dialog asynchronously with safety checks.
        """
        future = asyncio.get_running_loop().create_future()

        # 1. Success path: Dialog finishes normally
        def handle_finished(result):
            if not future.done():
                future.set_result(result)

        # 2. Safety path: If the dialog is destroyed before finishing
        def handle_destroyed():
            if not future.done():
                future.set_result(0) # 0 is QDialog.Rejected

        dialog.finished.connect(handle_finished)
        dialog.destroyed.connect(handle_destroyed)

        # open() is excellent because it is window-modal but non-blocking
        dialog.open() 
        
        try:
            return await future
        finally:
            # Disconnect signals to ensure no memory leaks/zombie calls
            try:
                dialog.finished.disconnect(handle_finished)
                dialog.destroyed.disconnect(handle_destroyed)
            except Exception:
                pass # Dialog might already be gone