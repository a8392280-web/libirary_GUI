**Libirary GUI**
A PySide6 desktop client for managing a personal media library. It connects to the Libirary backend API and lets you log in, browse, search, and organize items by status.

**Features**
- Categories: movies, series, games, books, manga, anime
- Status sections: in progress, planned, on hold, dropped, completed, favorites
- Grid or list view with sorting options
- Search dialog with debounced queries
- Random pick per section
- Detail view with rating and favorite updates
- External find links for movies (Cineby, VidSrc, ArabSeed, Akwam)
- Session refresh and secure token storage
- Update prompt via GitHub releases

**Tech Stack**
- PySide6 (Qt UI)
- qasync (async/await on the Qt event loop)
- httpx (async API client)
- keyring (secure refresh token storage)

**Requirements**
- Python 3.x
- An accessible Libirary backend API

**Setup**
1. `python -m venv venv`
2. `.\venv\Scripts\Activate.ps1` (PowerShell) or `.\venv\Scripts\activate` (cmd)
3. `pip install -r requirements.txt`
4. `python main.py`

**Configuration**
- Backend base URL: `app/api/api_client.py` in `LibraryAPIClient(base_url=...)`
- Update checker repo: `updater.py` (`GITHUB_USER`, `GITHUB_REPO`)

**Data Storage**
- Refresh token is stored in the OS keychain (keyring service name `MyLibraryApp`)
- Device ID is stored at `~/.library_app_device_id`
- UI settings are stored via QSettings (`MyLib` / `MyLibApp`)

**Project Layout**
- `app/` application code (api, presenters, views, services, utils)
- `resources/` Qt Designer UI files and icons
- `main.py` application entry point
- `updater.py` update check and prompt
- `version.py` app version
- `requirements.txt` Python dependencies

**Troubleshooting**
- If you see Qt thread-affinity errors, ensure all UI objects are created on the main thread. Network calls should run in background threads, while dialogs and widgets stay on the UI thread.

**License**
- Not specified yet
