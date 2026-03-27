# app/services/provider.py
from ..api.api_client import LibraryAPIClient
from ..api.auth_service import AuthService
from ..api.users_service import UserService
from ..api.user_media_service import UserMediaService
from ..api.media_service import MediaService

class ServiceProvider:
    def __init__(self):
        # The core client manages the session/token/device_id
        self.api_client = LibraryAPIClient()
        
        # Services use the shared client
        self.auth = AuthService(self.api_client)
        self.users = UserService(self.api_client)
        self.user_media = UserMediaService(self.api_client)
        self.media = MediaService(self.api_client)

    async def shutdown(self):
        await self.api_client.close()

# Create a single instance to be imported elsewhere
services = ServiceProvider()