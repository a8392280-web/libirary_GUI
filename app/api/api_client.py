import asyncio
import uuid
import httpx
import logging
from pathlib import Path
from ..models.models import ApiResponse
from ..config import API_BASE_URL, API_TIMEOUT, API_MAX_CONNECTIONS, DEVICE_ID_FILE, KEYRING_SERVICE_NAME, LOG_LEVEL

from app.utils.refresh_token_strore import save_refresh_token, get_refresh_token, delete_refresh_token
from asyncio import Semaphore

logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger("APIClient")

# Persists a stable device ID alongside the refresh-token store
_DEVICE_ID_FILE = DEVICE_ID_FILE


def _get_or_create_device_id() -> str:
    """Return the stored device ID, creating and persisting one if absent."""
    if _DEVICE_ID_FILE.exists():
        stored = _DEVICE_ID_FILE.read_text().strip()
        if stored:
            return stored
    device_id = str(uuid.uuid4())
    _DEVICE_ID_FILE.write_text(device_id)
    return device_id


# ─── API Client ─────────────────────────────────────────────────────────────

class LibraryAPIClient:
    def __init__(self, base_url: str = None):
        if base_url is None:
            base_url = API_BASE_URL
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(float(API_TIMEOUT)),
            limits=httpx.Limits(max_keepalive_connections=API_MAX_CONNECTIONS, keepalive_expiry=30.0)
        )
        self.access_token: str | None = None
        self._request_semaphore = Semaphore(10)
        self._device_id: str = _get_or_create_device_id()

    async def close(self):
        await self.client.aclose()

    # ─── STARTUP CHECK ───────────────────────────────────────────────

    async def check_startup_session(self) -> bool:
        stored_ref = get_refresh_token()
        if not stored_ref:
            logger.info("No refresh token found.")
            return False
        return await self._refresh_session(stored_ref)



    # ─── PRIVATE TOKEN REFRESH ───────────────────────────────────────────────

    async def _refresh_session(self, ref_token: str) -> bool:
        try:
            response = await self.client.post(
                "/auth/refresh",
                json={"refresh_token": ref_token},
                timeout=5.0,
            )
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                save_refresh_token(data["refresh_token"])
                logger.info("Token refreshed successfully.")
                return True
            delete_refresh_token()
            return False
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return False

    # ─── SMART REQUEST WRAPPER ───────────────────────────────────────────────

    async def request(
        self,
        method: str,
        endpoint: str,
        retry_on_401: bool = True,
        retry_on_network_error: bool = True,
        **kwargs,
    ) -> ApiResponse:
        async with self._request_semaphore:
            headers = kwargs.pop("headers", {})
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
            kwargs["headers"] = headers

            try:
                response = await self.client.request(method, endpoint, **kwargs)
            except (httpx.ReadError, httpx.ConnectError, httpx.RemoteProtocolError) as e:
                if retry_on_network_error:
                    await asyncio.sleep(0.5)
                    return await self.request(
                        method, endpoint,
                        retry_on_401=retry_on_401,
                        retry_on_network_error=False,
                        **kwargs,
                    )
                return ApiResponse(ok=False, status_code=0, error=f"Network error: {e}")
            except Exception as e:
                return ApiResponse(ok=False, status_code=0, error=str(e))

            if response.status_code == 401 and retry_on_401:
                stored_ref = get_refresh_token()
                if stored_ref and await self._refresh_session(stored_ref):
                    return await self.request(
                        method, endpoint,
                        retry_on_401=False,
                        retry_on_network_error=retry_on_network_error,
                        **kwargs,
                    )
                return ApiResponse(ok=False, status_code=401, error="Session expired. Please log in again.")

            try:
                data = response.json()
            except Exception:
                data = None

            return ApiResponse(
                ok=response.is_success,
                status_code=response.status_code,
                data=data,
                error=None if response.is_success else response.text,
            )

    # ─── CONVENIENCE METHODS ────────────────────────────────────────────────

    async def get(self, endpoint: str, retry_on_401: bool = True, **kwargs) -> ApiResponse:
        return await self.request("GET", endpoint, retry_on_401=retry_on_401, **kwargs)

    async def post(self, endpoint: str, retry_on_401: bool = True, **kwargs) -> ApiResponse:
        return await self.request("POST", endpoint, retry_on_401=retry_on_401, **kwargs)

    async def put(self, endpoint: str, retry_on_401: bool = True, **kwargs) -> ApiResponse:
        return await self.request("PUT", endpoint, retry_on_401=retry_on_401, **kwargs)

    async def patch(self, endpoint: str, retry_on_401: bool = True, **kwargs) -> ApiResponse:
        return await self.request("PATCH", endpoint, retry_on_401=retry_on_401, **kwargs)

    async def delete(self, endpoint: str, retry_on_401: bool = True, **kwargs) -> ApiResponse:
        return await self.request("DELETE", endpoint, retry_on_401=retry_on_401, **kwargs)
