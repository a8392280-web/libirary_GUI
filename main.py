import sys
from PySide6 import QtWidgets
import asyncio
from qasync import QEventLoop, asyncSlot
from updater import fetch_latest_release, show_update_dialog
from app.presenters.main_window_presenter import MainWidgetPresenter
from app.views.regester_view import RegesterView
from app.presenters.regester_presenter import RegesterPresenter
from app.services.providers import services
from app.views.main_window_view import MainWidgetView


class AppController:
    def __init__(self, api = services):
        self.api = api
        self.regester_view = None
        self.regester_presenter = None
        self.main_window = None

    async def start(self):
        """Initial check for session"""
        has_session = await self.api.api_client.check_startup_session()

        if has_session:
            self.show_main()
        else:
            self.show_login()

    def show_login(self):
        """Show the login window"""
        self.regester_view = RegesterView()
        self.regester_presenter = RegesterPresenter(self.regester_view, self.api)
        self.regester_view.login_success.connect(self.show_main)
        self.regester_view.show()

    def show_main(self):
        """Show the main window"""
        self.main_window_view = MainWidgetView()
        self.main_window_presenter = MainWidgetPresenter(self.main_window_view, self.api)
        self.main_window_view.logout_completed.connect(self.back_to_login)
        self.main_window_view.show()

        # Check for updates AFTER the window is visible
        # Fetch runs in a background thread so it never blocks the UI
        asyncio.create_task(self._check_updates_async())

        # Close the login window if it exists
        if self.regester_view:
            self.regester_view.close()
            self.regester_view = None
            self.regester_presenter = None

    async def _check_updates_async(self):
        """Runs the blocking network check in a thread; shows UI prompt on main thread."""
        info = await asyncio.to_thread(fetch_latest_release)
        if not info:
            return

        # If the window was closed while we were fetching, skip the dialog.
        if not hasattr(self, "main_window_view") or self.main_window_view is None:
            return

        latest_version, download_url = info
        show_update_dialog(self.main_window_view, latest_version, download_url)


    def back_to_login(self):
        """Switches from Main to Login"""
        # 1. Open the new window first so the app doesn't accidentally quit
        self.show_login()

        # 2. Close the old window using the CORRECT variable name
        if hasattr(self, 'main_window_view') and self.main_window_view:
            self.main_window_view.close()
            # Clean up the object to free memory
            self.main_window_view.deleteLater()
            self.main_window_view = None
            
        # 3. Also clear the presenter to avoid ghost tasks
        if hasattr(self, 'main_window_presenter'):
            self.main_window_presenter = None

    async def cleanup(self):
        """Clean up async resources before app closes"""
        await self.api.api_client.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    controller = AppController()

    with loop:
        loop.create_task(controller.start())
        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(controller.cleanup())
