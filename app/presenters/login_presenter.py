from qasync import asyncSlot


class AuthPresenter:
    """Handles business logic and coordinates between View and Model (API)"""
    
    def __init__(self, view, api_client):
        self.view = view
        self.api = api_client
        
        # Connect view signals to presenter methods
        self.view.signin_requested.connect(self.handle_signin)
        self.view.login_requested.connect(self.handle_login)
    
    @asyncSlot(str, str, str)
    async def handle_signin(self, name: str, email: str, password: str):
        """Handle sign up logic"""
        # Disable UI during request
        self.view.set_ui_enabled(False)
        
        try:
            print(f"Sign up - Name: {name}, Email: {email}")
            success = await self.api.register(name, email, password)
            
            if success:
                # Emit success signal (handled by AppController)
                self.view.login_success.emit()
                self.view.clear_inputs()
            else:
                self.view.show_critical_error(
                    "Could not create account. Email may already be registered."
                )
        except Exception as e:
            print(f"Registration error: {e}")
            self.view.show_critical_error(f"Registration failed: {str(e)}")
        finally:
            # Re-enable UI
            self.view.set_ui_enabled(True)
    
    @asyncSlot(str, str)
    async def handle_login(self, email: str, password: str):
        """Handle login logic"""
        # Disable UI during request
        self.view.set_ui_enabled(False)
        
        try:
            print(f"Log in - Email: {email}")
            success = await self.api.login(email, password)
            
            if success:
                print("Login success!")
                # Emit success signal (handled by AppController)
                self.view.login_success.emit()
                self.view.clear_inputs()
            else:
                self.view.show_error("Invalid username or password")
        except Exception as e:
            print(f"Login error: {e}")
            self.view.show_critical_error(f"Login failed: {str(e)}")
        finally:
            # Re-enable UI
            self.view.set_ui_enabled(True)