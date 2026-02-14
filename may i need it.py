
# class MainWidgetPresenter:
#     def __init__(self, view, api):
#         self.view = view
#         self.api = api
#         self.limit = 20
#         self.current_view_mode = "grid" # Keep track of the state
#         self.sort_by = "title"
#         self.order = "asc"

#         self.list_states = {
#             'movie_list_1': {'offset': 0, 'has_more': True, 'is_loading': False},
#             'movie_list_2': {'offset': 0, 'has_more': True, 'is_loading': False},
#             'movie_list_3': {'offset': 0, 'has_more': True, 'is_loading': False},
#             'movie_list_4': {'offset': 0, 'has_more': True, 'is_loading': False},
#             'movie_list_5': {'offset': 0, 'has_more': True, 'is_loading': False},
#             'movie_list_6': {'offset': 0, 'has_more': True, 'is_loading': False},
#         }
#         self.current_list = None


#         # ✅ Create separate models for each list to avoid conflicts
#         self.models = {
#             "in_progress": QStandardItemModel(),
#             "planned": QStandardItemModel(),
#             "on_hold": QStandardItemModel(),
#             "dropped": QStandardItemModel(),
#             "completed": QStandardItemModel(),
#             "favorites": QStandardItemModel(),
#         }

#         self.proxies = {}
#         self._setup_proxies()
        
#         self.delegate = MovieDelegate()
#         self.search_dialog = None
#         self.search_presenter = None
        
#         # ✅ Track which views have been connected to avoid duplicate signals
#         self._connected_views = set()

#         self._loading_lock = set()

#         # Connect View signals to presenter methods
#         self.view.logout_requested.connect(self.handle_logout)
#         self.view.search_requested.connect(self.show_search_dialog)
#         self.view.show_user_media.connect(self.handle_show_user_media)
#         self.view.random_media_requested.connect(self.handle_random_media_item)

#         self.view.show_home_requested.connect(lambda: self.view.set_current_index(0))
#         self.view.show_movies_requested.connect(lambda: self.view.set_current_index(1))
#         self.view.show_series_requested.connect(lambda: self.view.set_current_index(2))
#         self.view.show_games_requested.connect(lambda: self.view.set_current_index(3))
#         self.view.show_books_requested.connect(lambda: self.view.set_current_index(4))
#         self.view.show_comics_requested.connect(lambda: self.view.set_current_index(5))
#         self.view.show_setting_requested.connect(lambda: self.view.set_current_index(6))

#         self.view.near_bottom.connect(self.on_near_bottom)

#         self.view.ui.movies_view.clicked.connect(self.toggle_all_view_modes)



#     @asyncSlot()
#     async def handle_logout(self):
#         reply = QMessageBox.question(
#             self.view,
#             'Logout',
#             'Are you sure you want to logout?',
#             QMessageBox.Yes | QMessageBox.No
#         )

#         if reply == QMessageBox.Yes:
#             self.view.set_logout_enabled(False)
#             self.view.set_logout_text("Logging out...")

#             try:
#                 success = await self.api.logout()
#                 if not success:
#                     QMessageBox.warning(
#                         self.view,
#                         "Warning",
#                         "Server logout failed, but local session was cleared."
#                     )
#             except Exception as e:
#                 QMessageBox.critical(
#                     self.view,
#                     "Error",
#                     f"Logout error: {e}\nLocal session will be cleared."
#                 )
#             finally:
#                 self.view.set_logout_enabled(True)
#                 self.view.set_logout_text("Logout")
                
#     def _setup_proxies(self):
#         """Creates a proxy for each section and connects it to the View's search bars."""
        
#         # Use the dictionary you already created in the View
#         for section, search_bar in self.view.movies_search_line.items():
#             proxy = MultiFilterProxyModel()
#             proxy.setDynamicSortFilter(True) # <--- ADD THIS LINE
#             proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
            
#             # Link the View's search bar to this Presenter's proxy
#             search_bar.textChanged.connect(proxy.setFilterFixedString)
#             self.proxies[section] = proxy

#         # Assuming you have a dict in the view called self.movie_sort_combos
#         self.view.ui.movies_sort_by.currentIndexChanged.connect(lambda idx: self.handle_sort_change("movies", idx))
    


#     def handle_sort_change(self, section: str, index: int):
#         """Sorts ALL movie sections based on the single combo box selection."""
#         if index == 0:
#             self.sort_by = "title"
#             self.order = "asc"
#         elif index == 1:
#             self.sort_by = "title"
#             self.order = "desc"
#         elif index == 2:
#             self.sort_by = "released"
#             self.order = "asc"
#         elif index == 3:
#             self.sort_by = "released"
#             self.order = "desc"


#         for section in self.models.keys():
#             model = self.models.get(section)
#             model.clear()        

#         current_tab_index = self.view.ui.movies_tap_widget.currentIndex()
#         if current_tab_index == 0:
#             self.handle_show_user_media("movies", "in_progress", True)
#         elif current_tab_index == 1:
#             self.handle_show_user_media("movies", "planned", True)
#         elif current_tab_index == 2:
#             self.handle_show_user_media("movies", "on_hold", True)
#         elif current_tab_index == 3:
#             self.handle_show_user_media("movies", "dropped", True)
#         elif current_tab_index == 4:
#             self.handle_show_user_media("movies", "completed", True)
#         elif current_tab_index == 5:
#             self.handle_show_user_media("movies", "favorites", True)

#     def toggle_all_view_modes(self):
#         # 1. Flip the state
#         self.current_view_mode = "list" if self.current_view_mode == "grid" else "grid"

#         # 2. Apply to all 5 movie lists
#         views_dict = self.get_category_lists("movies")
#         for view in views_dict.values():
#             # Call the helper method you already added to your View
#             self.view.update_view_layout(view, self.current_view_mode)
            
#         print(f"Switched all views to: {self.current_view_mode}")


#     def show_search_dialog(self):
#         self.search_dialog = SearchView()
#         self.search_presenter = SearchPresenter(self.search_dialog, self.api)
#         self.search_dialog.exec()
#         if self.search_presenter:
#             self.search_presenter.cleanup()
#             self.search_presenter = None

#     def get_category_lists(self, category: str):
#         ui = self.view.ui
        
#         category_widgets = {
#             "movies": [
#                 ui.movies_list_1, 
#                 ui.movies_list_2, 
#                 ui.movies_list_3, 
#                 ui.movies_list_4, 
#                 ui.movies_list_5,
#                 ui.movies_list_6
#             ]
#         }
        

#         if category not in category_widgets:
#             raise ValueError(f"Unknown category: {category}")
        
#         widgets = category_widgets[category]
#         return {
#             "in_progress": widgets[0],
#             "planned":     widgets[1],
#             "on_hold":     widgets[2],
#             "dropped":     widgets[3],
#             "completed":   widgets[4],
#             "favorites":   widgets[5]
#         }

#     def handle_show_user_media(self, category: str, section: str, force: bool = False, offset: int = 0, limit: int =20):
#         """Wrapper to call async load_section from signal"""
#         asyncio.create_task(self.load_section(category, section, force= force, offset= offset, limit =limit))

#     async def load_section(self, category: str, section: str, force: bool = False, offset: int = 0, limit: int =20):

#         lock_id = f"{category}_{section}"

#         if lock_id in self._loading_lock:
#             print(f"Load for {lock_id} is already in progress. Skipping duplicate call.")
#             return
        
#         media_type_map = {
#                 "movies": "movie",
#                 "series": "series",
#                 "games": "game",
#                 "books": "book",
#                 "comics": "comic"
#             }

#         try:

#             self._loading_lock.add(lock_id)
            
#             media_type = media_type_map.get(category, "movie")

#             # ✅ Get the appropriate model for this section
#             model = self.models.get(section)
#             if model and model.rowCount() > 0 and not force:
#                 print(f"Items already exist in {section}. Skipping load.")
#                 return
            
#             model.clear()


#             if section == "favorites":
#                 url = f"users/me/media/?media_type={media_type}&favorite=true&sort_by={self.sort_by}&order={self.order}"
#             else:
#                 url = f"users/me/media/?media_type={media_type}&status={section}&sort_by={self.sort_by}&order={self.order}&offset={offset}&limit={limit}"

#             # Fetch data
#             data = await self.api.get(url)
            
            
#             # ✅ Add error handling
#             if not data:
#                 print(f"No data returned for {category}/{section}")
#                 return
        

#             target_view = self.get_category_lists(category)[section]

#             proxy = self.proxies.get(section)
            
#             if proxy:
#                 proxy.setSourceModel(model)
#                 target_view.setModel(proxy)
#             else:
#                 target_view.setModel(model)

#             # Setup the View (only connect signals once)
#             target_view.setItemDelegate(self.delegate)
#             self.view.update_view_layout(target_view, self.current_view_mode)
#             target_view.setMovement(QListView.Static)
#             target_view.setDragEnabled(False)
#             target_view.setAcceptDrops(False)
#             target_view.setEditTriggers(QListView.NoEditTriggers)
            
#             # ✅ Only connect click signal once per view
#             view_id = id(target_view)
#             if view_id not in self._connected_views:
#                 target_view.clicked.connect(self.handle_item_click)
#                 self._connected_views.add(view_id)

           
#             loader = get_image_loader()
            
#             for item in data:
#                 media = item.get("media", {})
                
#                 poster_url = media.get("cover_url", "")
                
#                 # Preload image into cache
#                 if poster_url:
#                     loader.load_image(
#                         poster_url,
#                         self.view.dumb_label,
#                         140,
#                         190
#                     )

#                 standard_item = QStandardItem()
#                 standard_item.setData(media.get("title"), Qt.UserRole + 1)
#                 standard_item.setData(media.get("released"), Qt.UserRole + 2)
#                 standard_item.setData(media.get("id"), Qt.UserRole + 4)
#                 standard_item.setData(poster_url, Qt.UserRole + 5)
#                 standard_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
#                 model.appendRow(standard_item)
        
#         except Exception as e:
#             print(f"Error loading section {category}/{section}: {e}")
#             import traceback
#             traceback.print_exc()
#             QMessageBox.warning(
#                 self.view,
#                 "Error",
#                 f"Failed to load {section} items: {str(e)}"
#             )
#         finally:
#             # Always take the shield down, even if the API fails
#             self._loading_lock.discard(lock_id)

#     def handle_item_click(self, index):
#         item_id = index.data(Qt.UserRole + 4)
#         if item_id:
#             print(f"Clicked item ID: {item_id}")
#             asyncio.create_task(self._show_detail(item_id))
    
#     async def _show_detail(self, item_id):
#         """✅ Now just delegates to the shared helper"""
#         await DialogHelper.show_detail_dialog(self.api, "movie", item_id)

#     def cleanup(self):
#         """✅ Fixed - removed non-existent attributes"""
#         if self.search_presenter:
#             self.search_presenter.cleanup()



#     def handle_random_media_item(self, category: str, section: str):

#         """Picks a random item from the currently visible (filtered) list."""
#         # 1. Get the proxy for the specific section
#         # Use the key format you established: self.proxies.get(section)
#         proxy = self.proxies.get(section)
        
#         # 2. Safety check: Is there anything visible to pick?
#         if not proxy or proxy.rowCount() == 0:
#             QMessageBox.information(
#                 self.view,
#                 "No Items",
#                 f"The current list is empty or filtered out. Nothing to pick!"
#             )
#             return

#         # 3. Pick a random row from the PROXY (visible rows only)
#         random_row = random.randint(0, proxy.rowCount() - 1)
        
#         # 4. Get the model index for that row
#         # Column 0 is where we stored our data
#         index = proxy.index(random_row, 0)
        
#         # 5. Extract the ID (UserRole + 4)
#         item_id = proxy.data(index, Qt.UserRole + 4)

#         if item_id:
#             print(f"Randomly selected visible ID: {item_id}")
#             # 6. Open the detail dialog
#             asyncio.create_task(self._show_detail(item_id))

#     def on_near_bottom(self, list_name):
#         # Business logic here
#         if self.is_loading or not self.has_more:
#             return
        
#         self.load_next_page(list_name)
    
#     def load_next_page(self, list_name):

#         print("Loading next page of items...")

#         offset = self.list_states[list_name]["offset"]
#         has_more = self.list_states[list_name]["has_more"]
#         is_loading = self.list_states[list_name]["is_loading"]

#         if is_loading or not has_more:
#             return

#         if list_name == "movie_list_2":
#             self.handle_show_user_media("movies","planned",)
#         # Fetch data from model
#         # Update view when done

#         self.list_states[list_name]["is_loading"] = False






















# # views/main_widget_view.py
# from PySide6.QtCore import Signal
# from PySide6.QtWidgets import QWidget, QLabel
# from resources.py_ui.main_ui import Ui_main_widget
# from PySide6.QtCore import QTimer
# from PySide6.QtCore import QSortFilterProxyModel, Qt
# from PySide6.QtWidgets import QListView

# class MainWidgetView(QWidget):
#     # Signals
#     logout_requested = Signal()
#     search_requested = Signal()
#     show_user_media = Signal(str, str, bool)  # category, section
#     random_media_requested = Signal(str, str)  # category, section
#     near_bottom = Signal(str)
    
#     # Optional: navigation signals
#     show_home_requested = Signal()
#     show_movies_requested = Signal()
#     show_series_requested = Signal()
#     show_games_requested = Signal()
#     show_books_requested = Signal()
#     show_comics_requested = Signal()
#     show_setting_requested = Signal()

#     def __init__(self):
#         super().__init__()
        
#         self.ui = Ui_main_widget()
#         self.ui.setupUi(self)
#         self.threshold = 100 # Threshold in pixels to trigger loading more items
        
#         self.movies_search_line = {
#                 "planned": self.ui.movies_search_2,
#                 "in_progress": self.ui.movies_search_1,
#                 "on_hold": self.ui.movies_search_3,
#                 "dropped": self.ui.movies_search_4,
#                 "completed": self.ui.movies_search_5,
#                 "favorites": self.ui.movies_search_6
#             }
        

#         self._setup_buttons()

#         self.dumb_label = QLabel("Dumb Label for Testing", self)
#         self.dumb_label.hide()  # Hide it as it's only for image loading tests
        
        
         

#     def _setup_buttons(self):
#         # Side buttons
#         self.ui.show_home.clicked.connect(lambda: self.show_home_requested.emit())
#         self.ui.show_movies.clicked.connect(lambda: self.show_movies_requested.emit())
#         self.ui.show_series.clicked.connect(lambda: self.show_series_requested.emit())
#         self.ui.show_games.clicked.connect(lambda: self.show_games_requested.emit())
#         self.ui.show_books.clicked.connect(lambda: self.show_books_requested.emit())
#         self.ui.show_comics.clicked.connect(lambda: self.show_comics_requested.emit())
#         self.ui.show_setting.clicked.connect(lambda: self.show_setting_requested.emit())

#         self.ui.show_movies.clicked.connect(lambda: self.set_user_media("movies", "in_progress"))
#         self.ui.movies_tap_widget.currentChanged.connect(self.on_tab_changed)


#         self.ui.refresh_button_1.clicked.connect(lambda: self.set_user_media("movies", "in_progress",True))
#         self.ui.refresh_button_2.clicked.connect(lambda: self.set_user_media("movies", "planned",True))
#         self.ui.refresh_button_3.clicked.connect(lambda: self.set_user_media("movies", "on_hold",True))
#         self.ui.refresh_button_4.clicked.connect(lambda: self.set_user_media("movies", "dropped",True))
#         self.ui.refresh_button_5.clicked.connect(lambda: self.set_user_media("movies", "completed",True))
#         self.ui.refresh_button_6.clicked.connect(lambda: self.set_user_media("movies", "favorites", True))


#         self.ui.movies_random_button_1.clicked.connect(lambda: self.random_media_requested.emit("movie", "in_progress"))
#         self.ui.movies_random_button_2.clicked.connect(lambda: self.random_media_requested.emit("movie", "planned"))
#         self.ui.movies_random_button_3.clicked.connect(lambda: self.random_media_requested.emit("movie", "on_hold"))
#         self.ui.movies_random_button_4.clicked.connect(lambda: self.random_media_requested.emit("movie", "dropped"))
#         self.ui.movies_random_button_5.clicked.connect(lambda: self.random_media_requested.emit("movie", "completed"))
#         self.ui.movies_random_button_6.clicked.connect(lambda: self.random_media_requested.emit("movie", "favorites"))


#         self.ui.movies_list_1.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("movies_list_1"))
#         self.ui.movies_list_2.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("movies_list_2"))
#         self.ui.movies_list_3.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("movies_list_3"))
#         self.ui.movies_list_4.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("movies_list_4"))
#         self.ui.movies_list_5.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("movies_list_5"))
#         self.ui.movies_list_6.verticalScrollBar().valueChanged.connect(lambda: self._check_scroll("movies_list_6"))





#         # Search button
#         self.ui.movies_add_botton.clicked.connect(lambda: self.search_requested.emit())

#         # Logout button
#         self.ui.logout.clicked.connect(lambda: self.logout_requested.emit())

#         # hide search bars initially
#         for line_edit in self.movies_search_line.values():
#             line_edit.hide()

#         self.ui.movies_sort_by.addItems([
#                 "Title (A-Z)",
#                 "Title (Z-A)",
#                 "Released (Oldest)",
#                 "Released (Newest)"
#             ])

        

#     def set_user_media(self, category: str, section: str, force: bool = False):
#         print(f"Emitting show_user_media with category: {category}, section: {section}, force: {force}")
#         self.show_user_media.emit(category, section, force)

#     # Methods to update UI
#     def set_current_index(self, index: int):
#         self.ui.stacked_body_Widget.setCurrentIndex(index)

#     def set_logout_enabled(self, enabled: bool):
#         self.ui.logout.setEnabled(enabled)

#     def set_logout_text(self, text: str):
#         self.ui.logout.setText(text)

#     def on_tab_changed(self, index):
#         """Called whenever user switches tabs"""
#         print(f"User switched to tab index: {index}")
        
#         if index == 0:
#             self.set_user_media("movies", "in_progress")
#         elif index == 1:
#             self.set_user_media("movies", "planned")
#         elif index == 2:
#            self.set_user_media("movies", "on_hold")
#         elif index == 3:
#            self.set_user_media("movies", "dropped")
#         elif index == 4:
#            self.set_user_media("movies", "completed")
#         elif index == 5:
#             self.set_user_media("movies", "favorites")


#     # app/views/main_widget_view.py

#     def update_view_layout(self, target_view, mode: str):
#         """Changes the QListView layout properties and resets them correctly."""
#         if mode == "grid":
#             # Reset to Grid settings
#             target_view.setViewMode(QListView.IconMode)
#             target_view.setFlow(QListView.LeftToRight) # Essential for grid wrapping
#             target_view.setResizeMode(QListView.Adjust)
#             target_view.setMovement(QListView.Static)
#             target_view.setWrapping(True)
#             target_view.setSpacing(15) # Give cards some breathing room
#         else:
#             # Reset to List settings
#             target_view.setViewMode(QListView.ListMode)
#             target_view.setFlow(QListView.TopToBottom) # Essential for vertical list
#             target_view.setResizeMode(QListView.Fixed)
#             target_view.setWrapping(False)
#             target_view.setSpacing(0)
        
#         # Force the view to recalculate item positions immediately
#         target_view.doItemsLayout()


#     def _check_scroll(self, list_name):
#         # Get the actual list widget using the name
#         list_widget = getattr(self.ui, list_name)
#         scrollbar = list_widget.verticalScrollBar()
        
#         if scrollbar.maximum() - scrollbar.value() < self.threshold:
#             self.near_bottom.emit(list_name)  # Pass which list triggered it
            