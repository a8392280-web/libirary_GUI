import asyncio
from PySide6.QtCore import QObject, QTimer
from qasync import asyncSlot

from app.views.search_card_view import MediaCard
from app.utils.image_loder import get_image_loader
from app.utils.dialog_helpers import DialogHelper

from app.config.providers import PROVIDERS

class SearchPresenter(QObject):
    DEBOUNCE_MS = 500

    def __init__(self, view, api_client):
        super().__init__()
        self.view = view
        self.api = api_client
        self.image_loader = get_image_loader()

        self._current_task = None
        self._is_db_mode = True

        # Debounce timer
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.handle_debounced_search)

        # Connections
        self.view.search_requested.connect(self.handle_search)
        self.view.source_changed.connect(self.on_source_changed)
        self.view.text_changed.connect(self.on_text_changed)

    # --------------------------------------------------
    # Source / Input Handling
    # --------------------------------------------------

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
    async def handle_search(self, query: str, media_type: str, source: str):
        await self._perform_search(query, media_type, source)

    # --------------------------------------------------
    # Core Search Logic
    # --------------------------------------------------

    async def _perform_search(self, query: str, media_type: str, source: str):

        media_type = media_type.lower()

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

    def _build_endpoint(self, query: str, media_type: str, source: str) -> str:
        media_type = media_type.lower()

        if source == "db":
            return f"media/{media_type}/search/?q={query}"

        provider = PROVIDERS.get(media_type)
        if not provider:
            raise ValueError(f"No provider configured for {media_type}")

        return f"fetch/{media_type}/{provider}?title={query}"


    async def _search_async(self, query: str, media_type: str, source: str):
        try:
            self.view.clear_results()

            endpoint = self._build_endpoint(query, media_type, source)
            response = await self.api.get(endpoint)

            if isinstance(response, list):
                await self._display_results(response, media_type)
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

            card = self._create_card(result)
            card.clicked.connect(
                lambda r=result, mt=media_type: self.on_card_clicked(mt, r)
            )

            self.view.add_search_result(card)
            self._load_cover(card, result.get("cover_url"))

            await asyncio.sleep(0.01)

    def _create_card(self, result: dict) -> MediaCard:
        return MediaCard(
            title=result.get("title", "Unknown"),
            cover_url=result.get("cover_url", ""),
            description=result.get("description", ""),
            released=result.get("released", ""),
            item_id=result.get("id"),
            tmdb_id=result.get("tmdb_id"),
            mal_id=result.get("mal_id"),
            ol_id=result.get("ol_id"),
            rawg_id=result.get("rawg_id"),
        )

    def _load_cover(self, card, url):
        if url and hasattr(card, "cover_label"):
            self.image_loader.load_image(
                url=url,
                label=card.cover_label,
                width=150,
                height=225,
                placeholder="⏳",
            )

    # --------------------------------------------------
    # Card Click
    # --------------------------------------------------

    def on_card_clicked(self, media_type: str, result: dict):
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
        await DialogHelper.show_detail_dialog(self.api, **ids)

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    def cancel_current_search(self):
        if self._current_task and not self._current_task.done():
            self._current_task.cancel()

    def cleanup(self):
        self.cancel_current_search()
        self.search_timer.stop()
