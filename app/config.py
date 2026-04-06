"""
Application Configuration
Loads environment variables from .env file for easy configuration management.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
ENV_FILE = Path(__file__).parent.parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    # Try parent directory
    ENV_FILE = Path(__file__).parent.parent.parent / ".env"
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)

# ─── API Configuration ──────────────────────────────────────────────────────

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000/v1/"
)
"""API endpoint URL for the Library backend"""

API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
"""HTTP request timeout in seconds"""

API_MAX_CONNECTIONS = int(os.getenv("API_MAX_CONNECTIONS", "20"))
"""Maximum number of concurrent HTTP connections"""

# ─── GitHub Configuration ──────────────────────────────────────────────────

GITHUB_USER = os.getenv("GITHUB_USER", "ahmed-x-dev")
"""GitHub username for update checks"""

GITHUB_REPO = os.getenv("GITHUB_REPO", "libirary_GUI")
"""GitHub repository name for update checks"""

# ─── Security Configuration ────────────────────────────────────────────────

KEYRING_SERVICE_NAME = os.getenv("KEYRING_SERVICE_NAME", "MyLibraryApp")
"""Service name for secure token storage in OS keyring"""

DEVICE_ID_FILE = Path.home() / os.getenv(
    "DEVICE_ID_FILE",
    ".library_app_device_id"
)
"""Path to store persistent device ID"""

# ─── Application Configuration ─────────────────────────────────────────────

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
"""Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"""

APP_NAME = os.getenv("APP_NAME", "MyLibraryApp")
"""Application name for QSettings"""

APP_ORG = os.getenv("APP_ORG", "MyLib")
"""Organization name for QSettings"""

# ─── Debug Mode ────────────────────────────────────────────────────────────

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
"""Enable debug mode (additional logging, etc.)"""
