import sys
from PySide6 import QtWidgets
from pathlib import Path
import socket
from app.Windows.main_window_controller import Widget
from resources.py_ui.login_ui import ModernAuthUI
from app.utils.refresh_token_strore import *
from app.api.client import LibraryAPIClient  # Our new service
import asyncio
from qasync import QEventLoop, asyncSlot

class AppController:
    def __init__(self):
        self.api = LibraryAPIClient()
        self.login_window = None
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
        self.login_window = ModernAuthUI(self.api)
        
        # Connect the signal to the switch function
        self.login_window.login_success.connect(self.show_main)
        self.login_window.show()
    
    def show_main(self):
        """Show the main window"""
        # Create the main window
        self.main_window = Widget(self.api)
        
        # Listen for the logout signal
        self.main_window.logout_requested.connect(self.back_to_login)
        self.main_window.show()
        
        # Close the login window if it exists
        if self.login_window:
            self.login_window.close()
            self.login_window = None
    
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