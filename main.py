import sys
from PySide6 import QtWidgets
import asyncio
from qasync import QEventLoop, asyncSlot

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
        """Initial check for session - now async"""
        # Check if we have a valid session
        has_session = await self.api.check_startup_session()
        
        if has_session:
            self.show_main()
        else:
            self.show_login()
    
    def show_login(self):
        """Show the login window"""
        # Create view
        self.login_view = AuthView()
        
        # Create presenter and connect it to view and model
        self.login_presenter = AuthPresenter(self.login_view, self.api)
        
        # Connect the success signal to the switch function
        self.login_view.login_success.connect(self.show_main)
        
        self.login_view.show()
    
    def show_main(self):
        """Show the main window"""

        self.main_window_view = MainWidgetView()
        self.main_window_presenter = MainWidgetPresenter(self.main_window_view, self.api)

        self.main_window_view.logout_requested.connect(self.back_to_login)
        self.main_window_view.show()

        # Close the login window if it exists
        if self.login_view:
            self.login_view.close()
            self.login_view = None
            self.login_presenter = None  # Clean up presenter
    
    @asyncSlot()
    async def back_to_login(self):
        """Switches from Main to Login - now async to handle logout"""
        # 1. Call the logout endpoint
        await self.api.logout()
        
        # 2. Open login screen
        self.show_login()
        
        # 3. Destroy main window
        if self.main_window:
            self.main_window.close()
            self.main_window = None
    
    async def cleanup(self):
        """Clean up async resources before app closes"""
        await self.api.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Set up the async event loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    # Create controller
    controller = AppController()
    
    # Start the app (async)
    with loop:
        # Schedule the async start
        loop.create_task(controller.start())
        
        # Run the event loop
        try:
            loop.run_forever()
        finally:
            # Clean up when app closes
            loop.run_until_complete(controller.cleanup())