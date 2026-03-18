import asyncio
import httpx
import logging
from dataclasses import dataclass
from typing import Any

from app.utils.refresh_token_strore import save_refresh_token, get_refresh_token, delete_refresh_token
from asyncio import Semaphore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APIClient")


# ─── Response Wrapper ─────────────────────────────────────────────────────────

@dataclass
class ApiResponse:
    """
    Unified response object returned by every request.
    Callers can always check .ok, .status_code, .data, and .error
    instead of getting raw JSON or None.
    """
    ok: bool
    status_code: int
    data: Any = None
    error: str = None


# ─── API Client ───────────────────────────────────────────────────────────────

class LibraryAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(10.0),
            limits=httpx.Limits(max_keepalive_connections=20, keepalive_expiry=30.0)
        )

        self.access_token: str | None = None
        self._request_semaphore = Semaphore(10)  # Max 10 concurrent requests

    async def close(self):
        """Call this when the app shuts down to cleanly close connections."""
        await self.client.aclose()

    # ─── 1. AUTHENTICATION & SESSION LOGIC ───────────────────────────────────

    async def check_startup_session(self) -> bool:
        """
        Called on app startup.
        If a refresh token exists in the OS keychain, silently exchange it
        for a new access token. Returns True if the user is still logged in.
        """
        stored_ref = get_refresh_token()
        if not stored_ref:
            logger.info("No refresh token found in keychain.")
            return False

        return await self._refresh_session(stored_ref)

    async def register(self, name: str, email: str, password: str, **extra_data) -> ApiResponse:
        """
        Register a new user, then auto-login on success.

        Note: Uses self.client directly (intentional) — registration does not
        need auth headers, semaphore, or 401 retry logic.
        """
        payload = {
            "username": name,
            "email": email,
            "password": password,
            **extra_data
        }
        try:
            response = await self.client.post("/auth/register", json=payload)

            if response.status_code == 201:
                logger.info("Registration successful. Auto-logging in...")
                return await self.login(email, password)

            logger.warning(f"Registration failed: {response.status_code}")
            return ApiResponse(ok=False, status_code=response.status_code, error="Registration failed")

        except Exception as e:
            logger.error(f"Registration error: {e}")
            return ApiResponse(ok=False, status_code=0, error=str(e))

    async def login(self, username: str, password: str) -> ApiResponse:
        """
        Login with username and password.
        On success, stores tokens and returns ApiResponse with user data.

        Note: Uses self.client directly (intentional) — login does not
        need auth headers, semaphore, or 401 retry logic.
        """
        try:
            # FastAPI OAuth2 expects form-data, NOT json
            response = await self.client.post(
                "/auth/login",
                data={"username": username, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                save_refresh_token(data["refresh_token"])
                logger.info("Login successful.")
                return ApiResponse(ok=True, status_code=200, data=data)

            logger.warning(f"Login failed: {response.status_code}")
            return ApiResponse(ok=False, status_code=response.status_code, error="Invalid credentials")

        except Exception as e:
            logger.error(f"Connection error during login: {e}")
            return ApiResponse(ok=False, status_code=0, error=str(e))

    async def logout(self) -> ApiResponse:
        """
        Logout the current user.
        1. Calls the server logout endpoint (best effort).
        2. Always clears local tokens regardless of server response.
        """
        server_response = await self.post("/auth/logout")

        # Always clear local session even if server call fails
        self.access_token = None
        delete_refresh_token()

        if server_response and server_response.ok:
            logger.info("Logout successful.")
            return ApiResponse(ok=True, status_code=server_response.status_code)

        logger.warning("Server logout failed, but local session cleared.")
        return ApiResponse(ok=True, status_code=0, error="Server logout failed, local session cleared")

    # ─── 2. INTERNAL TOKEN REFRESH ───────────────────────────────────────────

    async def _refresh_session(self, ref_token: str) -> bool:
        """
        Exchange a refresh token for a new access/refresh token pair.
        Uses token rotation — saves the new refresh token to keychain.
        Returns True on success, False if the session is dead.
        """
        try:
            # Explicit short timeout — don't let refresh hang the app
            response = await self.client.post(
                "/auth/refresh",
                json={"refresh_token": ref_token},
                timeout=5.0
            )

            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                save_refresh_token(data["refresh_token"])  # rotated token
                logger.info("Token refreshed successfully.")
                return True

            logger.warning("Refresh token expired or invalid. Clearing session.")
            delete_refresh_token()
            return False

        except Exception as e:
            logger.error(f"Error during token refresh: {e}")
            return False

    # ─── 3. SMART REQUEST WRAPPER ─────────────────────────────────────────────

    async def request(
        self,
        method: str,
        endpoint: str,
        retry_on_401: bool = True,
        retry_on_network_error: bool = True,
        **kwargs
    ) -> ApiResponse:
        """
        The core request method used by all API calls.

        Handles automatically:
        - Authorization headers (Bearer token)
        - Network-level retries (ReadError, ConnectError) — retries once
        - Silent token refresh on 401 — retries once with new token
        - Consistent ApiResponse return (never raw JSON or None)

        Args:
            method:                  HTTP method (GET, POST, PUT, DELETE)
            endpoint:                API path e.g. "/items"
            retry_on_401:            Internal flag — prevents infinite refresh loop
            retry_on_network_error:  Internal flag — prevents infinite retry loop
            **kwargs:                Passed directly to httpx (json=, data=, params=, etc.)
        """
        async with self._request_semaphore:

            # Attach Authorization header if we have a token
            headers = kwargs.pop("headers", {})
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
            kwargs["headers"] = headers

            # ── Attempt the request ───────────────────────────────────────────
            try:
                response = await self.client.request(method, endpoint, **kwargs)

            except (httpx.ReadError, httpx.ConnectError, httpx.RemoteProtocolError) as e:
                if retry_on_network_error:
                    logger.warning(f"Network error ({type(e).__name__}). Retrying once...")
                    await asyncio.sleep(0.5)
                    return await self.request(
                        method, endpoint,
                        retry_on_401=retry_on_401,
                        retry_on_network_error=False,
                        **kwargs
                    )
                logger.error(f"Network error persisted: {e}")
                return ApiResponse(ok=False, status_code=0, error=f"Network error: {e}")

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return ApiResponse(ok=False, status_code=0, error=str(e))

            # ── Handle 401: silent token refresh ─────────────────────────────
            # retry_on_401=False guard prevents an infinite refresh loop
            if response.status_code == 401 and retry_on_401:
                logger.info("401 detected. Attempting silent token refresh...")
                stored_ref = get_refresh_token()

                if stored_ref and await self._refresh_session(stored_ref):
                    logger.info("Retrying original request with refreshed token.")
                    return await self.request(
                        method, endpoint,
                        retry_on_401=False,   # ← prevents infinite loop
                        retry_on_network_error=retry_on_network_error,
                        **kwargs
                    )

                logger.error("Session is dead. User must re-authenticate.")
                return ApiResponse(ok=False, status_code=401, error="Session expired. Please log in again.")

            # ── Parse and return response ─────────────────────────────────────
            try:
                data = response.json()
            except Exception:
                logger.error(f"Failed to parse JSON. Status: {response.status_code}")
                data = None

            return ApiResponse(
                ok=response.is_success,
                status_code=response.status_code,
                data=data,
                error=None if response.is_success else str(data)
            )

    # ─── 4. CONVENIENCE HELPERS ───────────────────────────────────────────────

    async def get(self, endpoint: str, **kwargs) -> ApiResponse:
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> ApiResponse:
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> ApiResponse:
        return await self.request("PUT", endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs) -> ApiResponse:
        return await self.request("PATCH", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> ApiResponse:
        return await self.request("DELETE", endpoint, **kwargs)