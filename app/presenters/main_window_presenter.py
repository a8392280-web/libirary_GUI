# presenters/main_widget_presenter.py
from app.views.movie_delegate import MovieDelegate
from app.views.search_view import SearchView
from app.presenters.search_presenter import SearchPresenter
from app.utils.dialog_helpers import DialogHelper
from PySide6.QtWidgets import QMessageBox, QListView
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from qasync import asyncSlot
import asyncio
import random
from PySide6.QtCore import QTimer # Add to imports

class MainWidgetPresenter:
    # ✅ Single source of truth for sections
    SECTION_CONFIG = {
        "in_progress": {"index": 0, "widget_suffix": "1"},
        "planned":     {"index": 1, "widget_suffix": "2"},
        "on_hold":     {"index": 2, "widget_suffix": "3"},
        "dropped":     {"index": 3, "widget_suffix": "4"},
        "completed":   {"index": 4, "widget_suffix": "5"},
        "favorites":   {"index": 5, "widget_suffix": "6"},
    }

    def __init__(self, view, api):
        self.view = view
        self.api = api
        self.limit = 30
        self.current_view_mode = "grid"
        self.sort_by = "title"
        self.order = "asc"

        # ✅ Generate mappings dynamically from SECTION_CONFIG
        self.list_to_section = {
            f'movies_list_{cfg["widget_suffix"]}': section 
            for section, cfg in self.SECTION_CONFIG.items()
        }

        # ✅ Initialize states dynamically
        self.list_states = {
            section: {
                'offset': 0, 
                'has_more': True, 
                'is_loading': False, 
                'notified_end': False
            }
            for section in self.SECTION_CONFIG.keys()
        }

        # ✅ Initialize models dynamically
        self.models = {
            section: QStandardItemModel() 
            for section in self.SECTION_CONFIG.keys()
        }

        # REMOVED: self.proxies and _setup_proxies()
        
        self.delegate = MovieDelegate()
        self.search_dialog = None
        self.search_presenter = None
        self._views_setup = set()

        # Connect signals
        self.view.logout_requested.connect(self.handle_logout)
        self.view.add_requested.connect(self.show_search_dialog)
        self.view.show_user_media.connect(self.handle_show_user_media)
        self.view.random_media_requested.connect(self.handle_random_media_item)
        self.view.show_home_requested.connect(lambda: self.view.set_current_index(0))
        self.view.show_movies_requested.connect(lambda: self.view.set_current_index(1))
        # self.view.show_series_requested.connect(lambda: self.view.set_current_index(2))
        # self.view.show_games_requested.connect(lambda: self.view.set_current_index(3))
        # self.view.show_books_requested.connect(lambda: self.view.set_current_index(4))
        # self.view.show_comics_requested.connect(lambda: self.view.set_current_index(5))
        self.view.show_setting_requested.connect(lambda: self.view.set_current_index(2))
        self.view.near_bottom.connect(self.on_near_bottom)
        self.view.ui.view_button.clicked.connect(self.toggle_all_view_modes)
        
        # Connect sort directly
        self.view.ui.sort_button.currentIndexChanged.connect(lambda idx: self.handle_sort_change("movies", idx))


        self.search_timers = {}
        self.view.search_requested.connect(self.handle_search_input)

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
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    f"Logout error: {e}\nLocal session will be cleared."
                )
            finally:
                self.view.set_logout_enabled(True)
                self.view.set_logout_text("Logout")
                

    def handle_sort_change(self, section: str, index: int):
        """Sorts ALL movie sections based on the single combo box selection."""
        if index == 0:
            self.sort_by = "title"
            self.order = "asc"
        elif index == 1:
            self.sort_by = "title"
            self.order = "desc"
        elif index == 2:
            self.sort_by = "released"
            self.order = "asc"
        elif index == 3:
            self.sort_by = "released"
            self.order = "desc"

        # ✅ Clear all models and reset states dynamically
        for section_name in self.SECTION_CONFIG.keys():
            model = self.models[section_name]
            model.clear()
            state = self.list_states[section_name]
            state['offset'] = 0
            state['has_more'] = True
            state['is_loading'] = False
            state['notified_end'] = False

        # ✅ Reload current tab using config
        current_tab_index = self.view.ui.tap_widget.currentIndex()
        section = self.get_section_by_tab_index(current_tab_index)
        
        if section:
            self.handle_show_user_media("movies", section, True)

    def get_section_by_tab_index(self, tab_index: int):
        """Get section name from tab index using config"""
        for section, cfg in self.SECTION_CONFIG.items():
            if cfg["index"] == tab_index:
                return section
        return None

    def toggle_all_view_modes(self):
        self.current_view_mode = "list" if self.current_view_mode == "grid" else "grid"
        views_dict = self.get_category_lists("movies")
        for view in views_dict.values():
            self.view.update_view_layout(view, self.current_view_mode)
        print(f"Switched all views to: {self.current_view_mode}")

    def show_search_dialog(self):
        self.search_dialog = SearchView()
        self.search_presenter = SearchPresenter(self.search_dialog, self.api)
        self.search_dialog.exec()
        if self.search_presenter:
            self.search_presenter.cleanup()
            self.search_presenter = None

    def get_category_lists(self, category: str):
        """Get list widgets for a category"""
        ui = self.view.ui
        
        if category != "movies":
            raise ValueError(f"Unknown category: {category}")
        
        # ✅ Build dynamically from SECTION_CONFIG
        return {
            section: getattr(ui, f'list_view_{cfg["widget_suffix"]}')
            for section, cfg in self.SECTION_CONFIG.items()
        }

    def handle_show_user_media(self, category: str, section: str, force: bool = False, title : str = None):
        """Wrapper to call async load_section from signal"""
        # Quick return before creating async task
        if not force:
            model = self.models.get(section)
            state = self.list_states.get(section)
            if model and model.rowCount() > 0 and not state['is_loading']:
                print(f"Items already exist in {section}. Skipping load.")
                return
        
        asyncio.create_task(self.load_section(category, section, title = title))

    def _setup_view(self, category: str, section: str):
        """One-time view setup per section"""
        target_view = self.get_category_lists(category)[section]
        model = self.models[section]
        
        # ✅ Set model directly (No Proxy)
        target_view.setModel(model)
        
        target_view.setItemDelegate(self.delegate)
        self.view.update_view_layout(target_view, self.current_view_mode)
        target_view.setMovement(QListView.Static)
        target_view.setDragEnabled(False)
        target_view.setAcceptDrops(False)
        target_view.setEditTriggers(QListView.NoEditTriggers)
        target_view.clicked.connect(self.handle_item_click)

    async def load_section(self, category: str, section: str, append: bool = False, title : str = None):
        """
        Load a section with pagination support
        """
        media_type_map = {
            "movies": "movie",
            "series": "series",
            "games": "game",
            "books": "book",
            "comics": "comic"
        }

        state = self.list_states[section]
        
        # Single source of truth for loading state
        if state['is_loading']:
            print(f"Load for {section} already in progress. Skipping.")
            return

        try:
            state['is_loading'] = True
            
            media_type = media_type_map.get(category, "movie")
            model = self.models[section]

            # Setup view only once
            if section not in self._views_setup:
                self._setup_view(category, section)
                self._views_setup.add(section)

            # Initial load or force refresh: clear model and reset state
            if not append:
                model.clear()
                state['offset'] = 0
                state['has_more'] = True
                state['notified_end'] = False

            # Build API URL with pagination
            offset = state['offset']
            limit = self.limit

            # 1. Define the core parameters
            params = {
                "media_type": media_type,
                "sort_by": self.sort_by,
                "order": self.order,
                "offset": offset,
                "limit": self.limit
            }

            # Add conditional filters
            if section != "favorites":
                params["status"] = section
            else:
                params["favorite"] = "true"

            if title: # Only adds to URL if title is not None or empty
                params["title"] = title

            # API call
            data = await self.api.get("users/me/media/", params=params)
            
            if not data:
                print(f"No data returned for {category}/{section}")
                state['has_more'] = False
                return

            # Check if we have more data
            if len(data) < limit:
                state['has_more'] = False

            # Update offset for next load
            state['offset'] += len(data)

            # Add items to model (delegate handles image loading on-demand)
            for item in data:
                media = item.get("media", {})
                
                standard_item = QStandardItem()
                standard_item.setData(media.get("title"), Qt.UserRole + 1)
                standard_item.setData(media.get("released"), Qt.UserRole + 2)
                standard_item.setData(media.get("id"), Qt.UserRole + 4)
                standard_item.setData(media.get("cover_url", ""), Qt.UserRole + 5)
                standard_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
                model.appendRow(standard_item)
        
        except Exception as e:
            print(f"Error loading section {category}/{section}: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self.view, "Error", f"Failed to load {section} items: {str(e)}")
            state['has_more'] = False
        
        finally:
            state['is_loading'] = False

            # Check if we need to fill more space
            # We wait 300ms to ensure PySide has finished rendering the items
            if state['has_more']:
                QTimer.singleShot(300, lambda: self._ensure_screen_is_full(category, section))

    def on_near_bottom(self, list_name):
        """Called when user scrolls near bottom of a list"""
        section = self.list_to_section.get(list_name)
        
        if not section:
            print(f"Unknown list name: {list_name}")
            return

        state = self.list_states[section]
        
        if state['is_loading']:
            return
        
        if not state['has_more']:
            # Only print once when reaching the end
            if not state['notified_end']:
                print(f"No more data for {section}")
                state['notified_end'] = True
            return
        
        print(f"Loading next page for {section} (offset: {state['offset']})")
        self.load_next_page(section)
    
    def load_next_page(self, section):
        """Load next page while keeping the active search term"""
        title = self.list_states[section].get('current_search_title')
        asyncio.create_task(self.load_section("movies", section, append=True, title=title))

    def handle_item_click(self, index):
        item_id = index.data(Qt.UserRole + 4)
        if item_id:
            print(f"Clicked item ID: {item_id}")
            asyncio.create_task(self._show_detail(item_id))
    
    async def _show_detail(self, item_id):
        await DialogHelper.show_detail_dialog(self.api, "movie", item_id)

    def cleanup(self):
        if self.search_presenter:
            self.search_presenter.cleanup()


    def handle_random_media_item(self,category, section):
        asyncio.create_task(self.random_media_item(category, section))
                            
    async def random_media_item(self, category: str, section: str):
        
        """Picks a random item from the current list."""

        item = await self.api.get(f"users/me/media/random?media_type={category}&status={section}")

        if "detail" in item:
            QMessageBox.information(
                self.view,
                "No Items",
                "The current list is empty. Nothing to pick!"
            )
            return

        item_id = item.get("media").get("id")

        if item_id:
            print(f"Randomly selected ID: {item_id}")
            asyncio.create_task(self._show_detail(item_id))


    def handle_search_input(self, category, section, text):
        """Debounces the search input to avoid spamming the API"""
        # Create or restart a timer for this specific section
        if section not in self.search_timers:
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: self.execute_search(category, section))
            self.search_timers[section] = timer
        
        # Store the text in state so the timer-driven execution can find it
        self.list_states[section]['current_search_title'] = text
        self.search_timers[section].start(300) # 300ms delay

    def execute_search(self, category, section):
        """Performs the actual API reload"""
        search_text = self.list_states[section].get('current_search_title', "")
        # force=True to clear existing list and start from offset 0
        self.handle_show_user_media(category, section, force=True, title=search_text)

    def _ensure_screen_is_full(self, category, section):
        list_name = f'movies_list_{self.SECTION_CONFIG[section]["widget_suffix"]}'
        if self.view.is_list_starving(list_name):
            print(f"Screen still has empty space in {section}. Loading more...")
            self.load_next_page(section)