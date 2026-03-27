import logging
from ..models.models import ApiResponse

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, api_client):
        self.api = api_client

    async def register(self, username: str, email: str, password: str, **extra_data) -> ApiResponse:
        payload = {"username": username, "email": email, "password": password, **extra_data}
        response = await self.api.post("users/register", json=payload)
        if response.ok:
            logger.info("Registration successful.")
        return response

    async def verify_email(self, email: str, code: str) -> ApiResponse:
        """
        Verify an e-mail address.

        API schema: VerifyEmail { email: str, code: str (6 digits) }
        """
        response = await self.api.post(
            "users/verify-email",
            json={"email": email, "code": code},
        )
        return response

    async def resend_verification(self, email: str) -> ApiResponse:
        response = await self.api.post("users/resend-verification", json={"email": email})
        return response


    async def change_password(self, confirm_password: str, old_password: str, new_password: str) -> ApiResponse:
        payload = { "old_password": old_password, "new_password": new_password, "confirm_password": confirm_password }
        response = await self.api.post("users/change-password", json=payload)
        return response