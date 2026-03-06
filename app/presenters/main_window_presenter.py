# presenters/main_widget_presenter.py
from app.utils.image_loader import get_image_loader
from app.views.media_delegate import MediaDelegate
from app.views.search_view import SearchView
from app.presenters.search_presenter import SearchPresenter
from app.utils.dialog_helpers import DialogHelper
from PySide6.QtWidgets import QMessageBox, QListView
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem
from qasync import asyncSlot
import asyncio

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

        # ✅ Generate mappings dynamically
        self.list_to_section = {
            f'list_view_{cfg["widget_suffix"]}': section 
            for section, cfg in self.SECTION_CONFIG.items()
        }

        # ✅ Initialize states and models dynamically
        self.list_states = {
            section: {
                'offset': 0, 
                'has_more': True, 
                'is_loading': False, 
                'notified_end': False,
                'current_search_title': ""
            }
            for section in self.SECTION_CONFIG.keys()
        }

        self.models = {
            section: QStandardItemModel() 
            for section in self.SECTION_CONFIG.keys()
        }

        self.delegate = MediaDelegate()
        self.search_dialog = None
        self.search_presenter = None
        self._views_setup = set()
        self.search_timers = {}

        self._connect_signals()

    def _connect_signals(self):
        """Connects signals from the View"""
        self.view.logout_requested.connect(self.handle_logout)
        self.view.add_requested.connect(self.show_search_dialog)
        self.view.show_user_media.connect(self.handle_show_user_media)
        self.view.random_media_requested.connect(self.handle_random_media_item)
        self.view.near_bottom.connect(self.on_near_bottom)
        self.view.search_requested.connect(self.handle_search_input)
        
        # Navigation
        self.view.show_home_requested.connect(lambda: self.view.set_current_index(0))
        self.view.show_setting_requested.connect(lambda: self.view.set_current_index(2))
        
        # Layout & Sort
        self.view.ui.view_button.clicked.connect(self.toggle_all_view_modes)
        self.view.ui.sort_button.currentIndexChanged.connect(self.handle_sort_change)

        # Clear all data
        self.view.clear_all_data_requested.connect(self.clear_all_data)

    @asyncSlot()
    async def handle_logout(self):
        reply = QMessageBox.question(
            self.view, 'Logout', 'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.view.set_logout_enabled(False)
            self.view.set_logout_text("Logging out...")
            try:
                await self.api.logout()
            finally:
                self.view.set_logout_enabled(True)
                self.view.set_logout_text("Logout")

    def handle_sort_change(self, index: int):
        """Sorts ALL sections and reloads the active one."""
        sort_map = {
            0: ("title", "asc"),
            1: ("title", "desc"),
            2: ("released", "asc"),
            3: ("released", "desc")
        }
        self.sort_by, self.order = sort_map.get(index, ("title", "asc"))

        # Reset all models/states
        for section in self.SECTION_CONFIG.keys():
            self.models[section].clear()
            state = self.list_states[section]
            state.update({'offset': 0, 'has_more': True, 'is_loading': False, 'notified_end': False})

        # Reload the currently visible category/section
        self.handle_show_user_media(self.view.current_category, self.get_active_section(), True)

    def get_active_section(self):
        idx = self.view.ui.tap_widget.currentIndex()
        for section, cfg in self.SECTION_CONFIG.items():
            if cfg["index"] == idx: return section
        return "in_progress"

    def toggle_all_view_modes(self):
        self.current_view_mode = "list" if self.current_view_mode == "grid" else "grid"
        for section, cfg in self.SECTION_CONFIG.items():
            view = getattr(self.view.ui, f'list_view_{cfg["widget_suffix"]}')
            self.view.update_view_layout(view, self.current_view_mode)

    def handle_show_user_media(self, category: str, section: str, force: bool = False, title: str = None):
        if not force:
            model = self.models.get(section)
            if model and model.rowCount() > 0 and not self.list_states[section]['is_loading']:
                return
        
        asyncio.create_task(self.load_section(category, section, title=title))

    async def load_section(self, category: str, section: str, append: bool = False, title: str = None):
        state = self.list_states[section]
        if state['is_loading']: return

        try:
            state['is_loading'] = True
            model = self.models[section]

            if section not in self._views_setup:
                self._setup_view_widget(section)
                self._views_setup.add(section)

            if not append:
                model.clear()
                state.update({'offset': 0, 'has_more': True, 'notified_end': False})

            params = {
                "media_type": category,
                "sort_by": self.sort_by,
                "order": self.order,
                "offset": state['offset'],
                "limit": self.limit
            }

            if section == "favorites": params["favorite"] = "true"
            else: params["status"] = section

            if title: params["title"] = title

            response = await self.api.get("users/me/media/", params=params)
            data = response.get("data", []) if response else []

            if len(data) < self.limit:
                state['has_more'] = False

            state['offset'] += len(data)

            for item in data:
                standard_item = QStandardItem()
                standard_item.setData(item.get("title"), Qt.UserRole + 1)
                standard_item.setData(item.get("released"), Qt.UserRole + 2)
                standard_item.setData(item.get("id"), Qt.UserRole + 4)
                cover_url = item.get("cover_url", "")
                standard_item.setData(cover_url, Qt.UserRole + 5)
                standard_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                model.appendRow(standard_item)

                if cover_url:
                    get_image_loader().prefetch(cover_url)
        
        finally:
            state['is_loading'] = False
            if state['has_more']:
                QTimer.singleShot(300, lambda: self._ensure_screen_is_full(category, section))

    def _setup_view_widget(self, section: str):
        suffix = self.SECTION_CONFIG[section]["widget_suffix"]
        view = getattr(self.view.ui, f'list_view_{suffix}')
        view.setModel(self.models[section])
        view.setItemDelegate(self.delegate)
        self.view.update_view_layout(view, self.current_view_mode)
        view.clicked.connect(self.handle_item_click)

    def on_near_bottom(self, list_name):
        section = self.list_to_section.get(list_name)
        if not section or self.list_states[section]['is_loading'] or not self.list_states[section]['has_more']:
            return
        
        category = self.view.current_category
        title = self.list_states[section].get('current_search_title')
        asyncio.create_task(self.load_section(category, section, append=True, title=title))

    def handle_search_input(self, category, section, text):
        if section not in self.search_timers:
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: self.handle_show_user_media(category, section, force=True, title=self.list_states[section]['current_search_title']))
            self.search_timers[section] = timer
        
        self.list_states[section]['current_search_title'] = text
        self.search_timers[section].start(300)

    def handle_item_click(self, index):
        item_id = index.data(Qt.UserRole + 4)
        if item_id:
            asyncio.create_task(DialogHelper.show_detail_dialog(self.api, self.view.current_category, item_id))

    @asyncSlot()
    async def handle_random_media_item(self, category, section):
        print(f"Randomly selecting {category}/{section}")

        if section == "favorites":
            item = await self.api.get(f"users/me/media/random?media_type={category}&favorite=true")
        else:
            item = await self.api.get(f"users/me/media/random?media_type={category}&status={section}")

        if item and "id" in item:
            await DialogHelper.show_detail_dialog(self.api, category, item["id"])

    def _ensure_screen_is_full(self, category, section):
        list_name = f'list_view_{self.SECTION_CONFIG[section]["widget_suffix"]}'
        if self.view.is_list_starving(list_name):
            self.on_near_bottom(list_name)

    def show_search_dialog(self):
        self.search_dialog = SearchView()
        self.search_presenter = SearchPresenter(self.search_dialog, self.api)
        self.search_dialog.exec()


    def clear_all_data(self):
        """Resets all models and states to a clean slate."""
        for section in self.SECTION_CONFIG.keys():
            # 1. Clear the actual data model
            self.models[section].clear()
            
            # 2. Reset the tracking states (Pagination/Loading)
            self.list_states[section].update({
                'offset': 0,
                'has_more': True,
                'is_loading': False,
                'notified_end': False,
                'current_search_title': ""
            })

            # 3. Clear the UI search bars without triggering new searches
            search_bar = self.view.search_lines.get(section)
            if search_bar:
                search_bar.blockSignals(True)
                search_bar.clear()
                search_bar.blockSignals(False)
        
        print("All media lists cleared.")