import asyncio
from PySide6.QtCore import QObject, QTimer, Qt
from qasync import asyncSlot

from app.utils.dialog_helpers import DialogHelper
from app.utils.image_loader import get_image_loader

from app.services.providers import services

class SearchPresenter(QObject):
    DEBOUNCE_MS = 500

    def __init__(self, view, api = services):
        super().__init__()
        self.view = view
        self.api = api
        self.current_view_mode = "grid"

        self._current_task = None
        self._is_db_mode = True

        # Debounce timer
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.handle_debounced_search)

        # Connections
        self.view.search_requested.connect(self.handle_search)
        self.view.text_changed.connect(self.on_text_changed)
        self.view.ui.search_listView.clicked.connect(self._on_result_selected)

    # --------------------------------------------------
    # Source / Input Handling
    # --------------------------------------------------


    def on_text_changed(self, text):
        self.search_timer.stop()

        if not self._is_db_mode:
            return

        if not text.strip():
            self.view.clear_results()
            self.cancel_current_search()
            return

        self.search_timer.start(self.DEBOUNCE_MS)

    # --------------------------------------------------
    # Search Entry Points
    # --------------------------------------------------

    @asyncSlot()
    async def handle_debounced_search(self):
        if not self.view.validate_media_type():
            return

        await self._perform_search(
            query=self.view.get_search_text(),
            media_type=self.view.get_media_type().lower(),
            source="db",
        )

    @asyncSlot(str, str, str)
    async def handle_search(self, query: str, media_type: str):
        await self._perform_search(query, media_type)

    # --------------------------------------------------
    # Core Search Logic
    # --------------------------------------------------

    async def _perform_search(self, query: str, media_type: str):

        media_type = media_type.lower()

        self.cancel_current_search()
        self.view.set_loading(True)
        self.view.set_enabled(False)

        self._current_task = asyncio.create_task(
            self._search_async(query, media_type)
        )

        try:
            await self._current_task
        except asyncio.CancelledError:
            pass
        finally:
            self.view.set_loading(False)
            self.view.set_enabled(True)
            self._current_task = None


    async def _search_async(self, query: str, media_type: str):
        try:
            self.view.clear_results()

            response = await self.api.media.search_media(media_type, query)
            data = response.data if response and response.ok and response.data else []
            print(f"Raw search response: {data}")


            if isinstance(data, list):
                await self._display_results(data, media_type)
            else:
                print(f"No results for '{query}'")

        except Exception as e:
            print(f"Search error: {e}")
            self.view.show_error(f"Search failed: {str(e)}")

    # --------------------------------------------------
    # Display
    # --------------------------------------------------

    async def _display_results(self, results: list, media_type: str):
        for result in results:
            if asyncio.current_task().cancelled():
                break

            self.view.add_search_result(result)
            
            # Prefetch cover image
            cover_url = result.get("cover_url")
            if cover_url:
                get_image_loader().prefetch(cover_url)

            await asyncio.sleep(0.01)

    # --------------------------------------------------
    # Card Click
    # --------------------------------------------------

    def _on_result_selected(self, index):
        """Handle search result selection"""
        result = index.data(Qt.UserRole + 10)
        media_type = self.view.get_media_type().lower()
        
        if result:
            asyncio.create_task(
                self._show_detail(
                    media_type=media_type,
                    item_id=result.get("id"),
                    tmdb_id=result.get("tmdb_id"),
                    mal_id=result.get("mal_id"),
                    rawg_id=result.get("rawg_id"),
                    ol_id=result.get("ol_id"),
                )
            )

    async def _show_detail(self, **ids):
        await DialogHelper.show_detail_dialog(api=self.api, **ids)

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    def cancel_current_search(self):
        if self._current_task and not self._current_task.done():
            self._current_task.cancel()

    def cleanup(self):
        self.cancel_current_search()
        self.search_timer.stop()
