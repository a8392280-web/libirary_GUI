from app.utils.image_loder import get_image_loader
from app.utils.multi_filter_proxy import MultiFilterProxyModel
from app.views.movie_delegate import MovieDelegate
from app.views.search_view import SearchView
from app.presenters.search_presenter import SearchPresenter
from app.utils.dialog_helpers import DialogHelper  # ✅ Add this import
from PySide6.QtWidgets import QMessageBox, QListView
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from qasync import asyncSlot
import asyncio
import random


class MainWidgetPresenter:
    def __init__(self, view, api):
        self.view = view
        self.api = api
        
        # ✅ Create separate models for each list to avoid conflicts
        self.models = {
            "in_progress": QStandardItemModel(),
            "planned": QStandardItemModel(),
            "on_hold": QStandardItemModel(),
            "dropped": QStandardItemModel(),
            "completed": QStandardItemModel(),
        }

        self.proxies = {}
        self._setup_proxies()
        
        self.delegate = MovieDelegate()
        self.search_dialog = None
        self.search_presenter = None
        
        # ✅ Track which views have been connected to avoid duplicate signals
        self._connected_views = set()

        self._loading_lock = set()

        # Connect View signals to presenter methods
        self.view.logout_requested.connect(self.handle_logout)
        self.view.search_requested.connect(self.show_search_dialog)
        self.view.show_user_media.connect(self.handle_show_user_media)
        self.view.random_media_requested.connect(self.handle_random_media_item)

        self.view.show_home_requested.connect(lambda: self.view.set_current_index(0))
        self.view.show_movies_requested.connect(lambda: self.view.set_current_index(1))
        self.view.show_series_requested.connect(lambda: self.view.set_current_index(2))
        self.view.show_games_requested.connect(lambda: self.view.set_current_index(3))
        self.view.show_books_requested.connect(lambda: self.view.set_current_index(4))
        self.view.show_comics_requested.connect(lambda: self.view.set_current_index(5))
        self.view.show_setting_requested.connect(lambda: self.view.set_current_index(6))


        self.view.ui.movies_view.clicked.connect(self.toggle_all_view_modes)
        self.current_view_mode = "grid" # Keep track of the state


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
                
    def _setup_proxies(self):
        """Creates a proxy for each section and connects it to the View's search bars."""
        
        # Use the dictionary you already created in the View
        for section, search_bar in self.view.movies_search_line.items():
            proxy = MultiFilterProxyModel()
            proxy.setDynamicSortFilter(True) # <--- ADD THIS LINE
            proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
            
            # Link the View's search bar to this Presenter's proxy
            search_bar.textChanged.connect(proxy.setFilterFixedString)
            self.proxies[section] = proxy

        # Assuming you have a dict in the view called self.movie_sort_combos
        self.view.ui.movies_sort_by.currentIndexChanged.connect(lambda idx: self.handle_sort_change("movies", idx))
    


    def handle_sort_change(self, section: str, index: int):
        """Sorts ALL movie sections based on the single combo box selection."""
        
        # We ignore the 'section' argument and loop through all known proxies
        for section_name, proxy in self.proxies.items():
            if not proxy:
                continue

            # Apply the sorting logic to every proxy
            if index == 0: # Title A-Z
                proxy.setSortRole(Qt.UserRole + 1)
                proxy.sort(0, Qt.AscendingOrder)
            elif index == 1: # Title Z-A
                proxy.setSortRole(Qt.UserRole + 1)
                proxy.sort(0, Qt.DescendingOrder)
            elif index == 2: # Released (Oldest)
                proxy.setSortRole(Qt.UserRole + 2)
                proxy.sort(0, Qt.AscendingOrder)
            elif index == 3: # Released (Newest)
                proxy.setSortRole(Qt.UserRole + 2)
                proxy.sort(0, Qt.DescendingOrder)
                
        print(f"Global sort applied to all sections (Option {index})")

    def toggle_all_view_modes(self):
        # 1. Flip the state
        self.current_view_mode = "list" if self.current_view_mode == "grid" else "grid"

        # 2. Apply to all 5 movie lists
        views_dict = self.get_category_lists("movies")
        for view in views_dict.values():
            # Call the helper method you already added to your View
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
        ui = self.view.ui
        
        category_widgets = {
            "movies": [
                ui.movies_list_1, 
                ui.movies_list_2, 
                ui.movies_list_3, 
                ui.movies_list_4, 
                ui.movies_list_5
            ]
        }
        

        if category not in category_widgets:
            raise ValueError(f"Unknown category: {category}")
        
        widgets = category_widgets[category]
        return {
            "in_progress": widgets[0],
            "planned":     widgets[1],
            "on_hold":     widgets[2],
            "dropped":     widgets[3],
            "completed":   widgets[4],
        }

    def handle_show_user_media(self, category: str, section: str, force: bool = False):
        """Wrapper to call async load_section from signal"""
        asyncio.create_task(self.load_section(category, section, force= force))

    async def load_section(self, category: str, section: str, force: bool = False):

        lock_id = f"{category}_{section}"

        if lock_id in self._loading_lock:
            print(f"Load for {lock_id} is already in progress. Skipping duplicate call.")
            return
        
        media_type_map = {
                "movies": "movie",
                "series": "series",
                "games": "game",
                "books": "book",
                "comics": "comic"
            }

        try:

            self._loading_lock.add(lock_id)
            
            media_type = media_type_map.get(category, "movie")

            # ✅ Get the appropriate model for this section
            model = self.models.get(section)
            if model and model.rowCount() > 0 and not force:
                print(f"Items already exist in {section}. Skipping load.")
                return
            
            model.clear()


            # Fetch data
            data = await self.api.get(
                f"users/me/media/?media_type={media_type}&status={section}"
            )
            
            # ✅ Add error handling
            if not data:
                print(f"No data returned for {category}/{section}")
                return
        

            target_view = self.get_category_lists(category)[section]

            proxy = self.proxies.get(section)
            
            if proxy:
                proxy.setSourceModel(model)
                target_view.setModel(proxy)
            else:
                target_view.setModel(model)

            # Setup the View (only connect signals once)
            target_view.setItemDelegate(self.delegate)
            self.view.update_view_layout(target_view, self.current_view_mode)
            target_view.setMovement(QListView.Static)
            target_view.setDragEnabled(False)
            target_view.setAcceptDrops(False)
            target_view.setEditTriggers(QListView.NoEditTriggers)
            
            # ✅ Only connect click signal once per view
            view_id = id(target_view)
            if view_id not in self._connected_views:
                target_view.clicked.connect(self.handle_item_click)
                self._connected_views.add(view_id)

           
            loader = get_image_loader()
            
            for item in data:
                media = item.get("media", {})
                
                poster_url = media.get("cover_url", "")
                
                # Preload image into cache
                if poster_url:
                    loader.load_image(
                        poster_url,
                        self.view.dumb_label,
                        140,
                        190
                    )

                standard_item = QStandardItem()
                standard_item.setData(media.get("title"), Qt.UserRole + 1)
                standard_item.setData(media.get("released"), Qt.UserRole + 2)
                standard_item.setData(media.get("id"), Qt.UserRole + 4)
                standard_item.setData(poster_url, Qt.UserRole + 5)
                standard_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
                model.appendRow(standard_item)
        
        except Exception as e:
            print(f"Error loading section {category}/{section}: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(
                self.view,
                "Error",
                f"Failed to load {section} items: {str(e)}"
            )
        finally:
            # Always take the shield down, even if the API fails
            self._loading_lock.discard(lock_id)

    def handle_item_click(self, index):
        item_id = index.data(Qt.UserRole + 4)
        if item_id:
            print(f"Clicked item ID: {item_id}")
            asyncio.create_task(self._show_detail(item_id))
    
    async def _show_detail(self, item_id):
        """✅ Now just delegates to the shared helper"""
        await DialogHelper.show_detail_dialog(self.api, "movie", item_id)

    def cleanup(self):
        """✅ Fixed - removed non-existent attributes"""
        if self.search_presenter:
            self.search_presenter.cleanup()



    def handle_random_media_item(self, category: str, section: str):

        """Picks a random item from the currently visible (filtered) list."""
        # 1. Get the proxy for the specific section
        # Use the key format you established: self.proxies.get(section)
        proxy = self.proxies.get(section)
        
        # 2. Safety check: Is there anything visible to pick?
        if not proxy or proxy.rowCount() == 0:
            QMessageBox.information(
                self.view,
                "No Items",
                f"The current list is empty or filtered out. Nothing to pick!"
            )
            return

        # 3. Pick a random row from the PROXY (visible rows only)
        random_row = random.randint(0, proxy.rowCount() - 1)
        
        # 4. Get the model index for that row
        # Column 0 is where we stored our data
        index = proxy.index(random_row, 0)
        
        # 5. Extract the ID (UserRole + 4)
        item_id = proxy.data(index, Qt.UserRole + 4)

        if item_id:
            print(f"Randomly selected visible ID: {item_id}")
            # 6. Open the detail dialog
            asyncio.create_task(self._show_detail(item_id))