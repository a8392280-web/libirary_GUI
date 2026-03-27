import logging
from ..models.models import ApiResponse
from app.utils.refresh_token_strore import save_refresh_token, get_refresh_token, delete_refresh_token

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, api_client):
        self.api = api_client


    async def login(self, email: str, password: str) -> ApiResponse:
        """
        Login via JSON body.

        API schema: LoginRequest { email, password, device_id }
        The device_id is managed internally and persisted between sessions.
        """
        payload = {
            "email": email,
            "password": password,
            "device_id": self.api._device_id,
        }
        response = await self.api.post("auth/login", json=payload)
        if response.ok:
            data = response.data
            if isinstance(data, dict):
                access_token = data.get("access_token")
                refresh_token = data.get("refresh_token")
                if access_token:
                    self.api.access_token = access_token
                if refresh_token:
                    save_refresh_token(refresh_token)
            logger.info("Login successful.")
        return response

    async def logout(self) -> ApiResponse:
        """
        Logout current device.

        API requires the refresh token in the request body:
        RefreshRequest { refresh_token: str }
        """
        refresh_token = get_refresh_token()
        resp = await self.api.post(
            "auth/logout",
            json={"refresh_token": refresh_token} if refresh_token else {},
        )
        self.api.access_token = None
        delete_refresh_token()
        return resp

    async def logout_all(self) -> ApiResponse:
        resp = await self.api.post("auth/logout-all")
        self.api.access_token = None
        delete_refresh_token()
        return resp
