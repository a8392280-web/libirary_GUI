import webbrowser
import requests
from packaging import version
from PySide6.QtWidgets import QMessageBox
from version import __version__
from app.config import GITHUB_USER, GITHUB_REPO


def fetch_latest_release():
    """
    Fetch the latest release info from GitHub.
    Returns (latest_version, download_url) or None if unavailable.
    """
    try:
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None  # No release published yet or network issue

        data = response.json()
        latest_version = data["tag_name"].lstrip("v")
        download_url = data["html_url"]

        return latest_version, download_url

    except Exception as e:
        # Network down, timeout, etc. - never crash the app over an update check
        print(f"Update check failed: {e}")
        return None


def show_update_dialog(parent, latest_version: str, download_url: str):
    """
    Show the update prompt on the UI thread.
    """
    if version.parse(latest_version) <= version.parse(__version__):
        return

    msg = QMessageBox(parent)
    msg.setWindowTitle("Update Available")
    msg.setText(
        f"A new version (v{latest_version}) is available!\n"
        f"You are currently on v{__version__}."
    )
    msg.setInformativeText("Would you like to open the download page?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.Yes)

    if msg.exec() == QMessageBox.Yes:
        webbrowser.open(download_url)


def check_for_updates(parent=None):
    """
    Checks GitHub releases for a newer version.
    Shows a dialog if an update is available.
    Silently does nothing if already up to date or if check fails.

    Note: This is synchronous and should run on the UI thread.
    """
    info = fetch_latest_release()
    if not info:
        return
    latest_version, download_url = info
    show_update_dialog(parent, latest_version, download_url)
