import asyncio
from PySide6.QtCore import QObject, QTimer, Qt
from PySide6.QtWidgets import QMessageBox
from qasync import asyncSlot
from app.views.search_card_view import MediaCard
from app.utils.image_loder import get_image_loader
from app.utils.dialog_helpers import DialogHelper 


class SearchPresenter(QObject):
    def __init__(self, view, api_client):
        super().__init__()
        self.view = view
        self.api = api_client
        self.image_loader = get_image_loader()
        
        # Debounce timer
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.handle_debounced_search)
        
        self._current_task = None
        self._is_db_mode = True
        
        # Connections
        self.view.search_requested.connect(self.handle_search)
        self.view.source_changed.connect(self.on_source_changed)
        self.view.text_changed.connect(self.on_text_changed)

    def on_source_changed(self, index):
        self._is_db_mode = (index == 0)
        self.cancel_current_search()
    
    def on_text_changed(self, text):
        self.search_timer.stop()
        if not self._is_db_mode:
            return
        
        if not text.strip():
            self.view.clear_results()
            self.cancel_current_search()
            return
        
        self.search_timer.start(500)

    @asyncSlot()
    async def handle_debounced_search(self):
        if not self.view.validate_media_type():
            return
        
        query = self.view.get_search_text()
        media_type = self.view.get_media_type()
        await self._perform_search(query, media_type, "db")

    @asyncSlot(str, str, str)
    async def handle_search(self, query: str, media_type: str, source: str):
        await self._perform_search(query, media_type, source)

    async def _perform_search(self, query: str, media_type: str, source: str):
        self.cancel_current_search()
        self.view.set_enabled(False)
        
        self._current_task = asyncio.create_task(
            self._search_async(query, media_type, source)
        )
        
        try:
            await self._current_task
        except asyncio.CancelledError:
            pass
        finally:
            self.view.set_enabled(True)
            self._current_task = None

    async def _search_async(self, query: str, media_type: str, source: str):
        try:
            self.view.clear_results()
            
            # API Routing
            endpoint = f"media/movies/search/?q={query}" if source == "db" \
                       else f"media/movies/api-search/tmdb?title={query}"
            
            response = await self.api.get(endpoint)
            
            if response and isinstance(response, list):
                await self._display_results(response)
            else:
                print(f"No results for '{query}'")
                
        except Exception as e:
            print(f"Search error: {e}")
            self.view.show_error(f"Search failed: {str(e)}")

    async def _display_results(self, results: list):
        for result in results:
            if asyncio.current_task().cancelled():
                break
            
            card = MediaCard(
                title=result.get("title", "Unknown"),
                cover_url=result.get("cover_url", ""),
                description=result.get("description", ""),
                released=result.get("released", ""),
                item_id=result.get("id")
            )
            
            # Use a helper to avoid closure issues and handle clicks
            card.clicked.connect(lambda i=result.get("id"): self.on_card_clicked(i))
            
            self.view.add_search_result(card)

            # Async Image Loading
            if result.get("cover_url") and hasattr(card, 'cover_label'):
                self.image_loader.load_image(
                    url=result.get("cover_url"),
                    label=card.cover_label,
                    width=150,
                    height=225,
                    placeholder="⏳"
                )
            
            # Yield to event loop to keep UI smooth
            await asyncio.sleep(0.01)

    def on_card_clicked(self, item_id):
        """Bridge Qt Signal to Async Task"""
        if item_id:
            asyncio.create_task(self._show_detail(item_id))
    
    async def _show_detail(self, item_id):
        """✅ Now just delegates to the shared helper"""
        await DialogHelper.show_detail_dialog(self.api, "movie", item_id)

    def cancel_current_search(self):
        if self._current_task and not self._current_task.done():
            self._current_task.cancel()

    def cleanup(self):
        self.cancel_current_search()
        self.search_timer.stop()