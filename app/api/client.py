import httpx
import logging
from app.utils.refresh_token_strore import save_refresh_token, get_refresh_token, delete_refresh_token
from asyncio import Semaphore

# Setup logging to see token refreshes in your console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APIClient")

class LibraryAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        # We use AsyncClient for async operations
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(10.0), # Prevent hanging forever
            limits=httpx.Limits(max_keepalive_connections=20)
        )

        self.access_token = None
        self._request_semaphore = Semaphore(10)  # Max 10 concurrent requests
    async def close(self):
        """Close the async client when done."""
        await self.client.aclose()

    # --- 1. AUTHENTICATION & SESSION LOGIC ---

    async def check_startup_session(self) -> bool:
        """
        Checks if a refresh token exists and attempts to get a new access token.
        Used in main.py to decide which window to show.
        """
        stored_ref = get_refresh_token()
        if not stored_ref:
            logger.info("No refresh token found in keychain.")
            return False
        
        return await self._refresh_session(stored_ref)
    
    async def register(self, name, email, password, **extra_data) -> bool:
        """
        Calls the user creation endpoint.
        """
        payload = {
            "username": name,
            "email": email,
            "password": password,
            **extra_data  # Any other fields like 'full_name'
        }
        try:
            # Note: Registration usually takes a JSON body
            response = await self.client.post("/users/add", json=payload)
            
            if response.status_code == 201:  # 201 Created
                logger.info("Registration successful.")
                # AUTO-LOGIN: After registering, call the login method
                return await self.login(email, password)
            
            return False
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False
        
    async def login(self, username, password) -> bool:
        """
        Calls the login endpoint. On success, saves tokens.
        Used by ModernAuthUI.
        """
        try:
            # FastAPI OAuth2 uses form-data, so we use 'data' instead of 'json'
            response = await self.client.post(
                "/auth/login", 
                data={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                # Save the raw refresh token string to OS Keychain
                save_refresh_token(data["refresh_token"])
                logger.info("Login successful.")
                return True
            
            logger.warning(f"Login failed: {response.status_code}")
            return False
        except Exception as e:
            logger.error(f"Connection error during login: {e}")
            return False

    async def logout(self) -> bool:
        """Clears session on server, local keychain, and RAM."""
        try:
            # 1. Call the FastAPI logout endpoint (requires auth)
            # This triggers your router.post("/logout") in the backend
            response = await self.post("/auth/logout")
            success = response.status_code == 204
        except Exception as e:
            print(f"Server logout failed: {e}")
            success = False

        # 2. Always clear local data even if the server call fails
        self.access_token = None
        delete_refresh_token() 
        return success
    
    # --- 2. THE INTERNAL REFRESH LOGIC ---

    async def _refresh_session(self, ref_token: str) -> bool:
        """
        Exchange a refresh token for a new access/refresh pair (Rotation).
        """
        try:
            # Your FastAPI endpoint expects 'refresh_token' in the JSON body
            response = await self.client.post(
                "/auth/refresh", 
                json={"refresh_token": ref_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                # Update the keychain with the NEW rotated refresh token
                save_refresh_token(data["refresh_token"])
                logger.info("Token refreshed successfully.")
                return True
            
            logger.warning("Refresh token expired or invalid.")
            delete_refresh_token()
            return False
        except Exception as e:
            logger.error(f"Error during token refresh: {e}")
            return False

    # --- 3. THE SMART REQUEST WRAPPER ---

    async def request(self, method, endpoint, **kwargs):
        async with self._request_semaphore:
            """
            The main method to call your API.
            Handles Authorization headers and automatic 401 retries.
            """
            # Ensure headers exist and add the Bearer token
            headers = kwargs.get("headers", {})
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
            kwargs["headers"] = headers

            # 1. Attempt the request
            response = await self.client.request(method, endpoint, **kwargs)

            # 2. If 401, try to refresh once
            if response.status_code == 401:
                logger.info("401 Detected. Attempting silent refresh...")
                stored_ref = get_refresh_token()
                
                if stored_ref and await self._refresh_session(stored_ref):
                    # 3. If refresh worked, update header and retry
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    kwargs["headers"] = headers
                    logger.info("Retrying original request with new token.")
                    return await self.client.request(method, endpoint, **kwargs)
                else:
                    logger.error("Session dead. User must re-authenticate.")
                    # Optional: You could emit a PySide signal here to show the login screen
            
            return response.json()

    # Helper methods for easier calls
    async def get(self, endpoint, **kwargs):
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint, **kwargs):
        return await self.request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self.request("DELETE", endpoint, **kwargs)