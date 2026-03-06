import sys
from PySide6 import QtWidgets
import asyncio
from qasync import QEventLoop, asyncSlot
from updater import check_for_updates
from app.presenters.main_window_presenter import MainWidgetPresenter
from app.views.login_view import AuthView
from app.presenters.login_presenter import AuthPresenter
from app.api.client import LibraryAPIClient
from app.views.main_window_view import MainWidgetView


class AppController:
    def __init__(self):
        self.api = LibraryAPIClient()
        self.login_view = None
        self.login_presenter = None
        self.main_window = None

    async def start(self):
        """Initial check for session"""
        has_session = await self.api.check_startup_session()

        if has_session:
            self.show_main()
        else:
            self.show_login()

    def show_login(self):
        """Show the login window"""
        self.login_view = AuthView()
        self.login_presenter = AuthPresenter(self.login_view, self.api)
        self.login_view.login_success.connect(self.show_main)
        self.login_view.show()

    def show_main(self):
        """Show the main window"""
        self.main_window_view = MainWidgetView()
        self.main_window_presenter = MainWidgetPresenter(self.main_window_view, self.api)
        self.main_window_view.logout_requested.connect(self.back_to_login)
        self.main_window_view.show()

        # ✅ Check for updates AFTER the window is visible
        # Runs in a background thread so it never blocks the UI
        asyncio.create_task(self._check_updates_async())

        # Close the login window if it exists
        if self.login_view:
            self.login_view.close()
            self.login_view = None
            self.login_presenter = None

    async def _check_updates_async(self):
        """Runs the blocking update check in a thread so UI stays responsive."""
        await asyncio.to_thread(check_for_updates, self.main_window_view)

    @asyncSlot()
    async def back_to_login(self):
        """Switches from Main to Login"""
        await self.api.logout()
        self.show_login()

        if self.main_window:
            self.main_window.close()
            self.main_window = None

    async def cleanup(self):
        """Clean up async resources before app closes"""
        await self.api.close()


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