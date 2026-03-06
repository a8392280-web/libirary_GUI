import hashlib
from pathlib import Path
from platformdirs import user_cache_dir
from PySide6.QtCore import QUrl, Qt, QObject, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


# ------------------------------------------------------------------
# 📁 Cache directory helper
# ------------------------------------------------------------------
def _get_writable_cache_dir() -> Path:
    """
    Returns the OS-appropriate cache directory for poster images.
    Works correctly both as a .py script and as a PyInstaller .exe.

    Windows : C:\\Users\\<user>\\AppData\\Local\\MyLib\\Cache\\posters
    macOS   : ~/Library/Caches/MyLib/posters
    Linux   : ~/.cache/MyLib/posters
    """
    cache = Path(user_cache_dir(appname="MyLib", appauthor="Ahmos")) / "posters"
    cache.mkdir(parents=True, exist_ok=True)
    return cache


# ------------------------------------------------------------------
# 🪣 Dummy label — absorbs label calls during prefetch
# ------------------------------------------------------------------
class _DummyLabel:
    """Absorbs label calls during prefetch — nothing is displayed."""
    def setText(self, *a): pass
    def setAlignment(self, *a): pass
    def setStyleSheet(self, *a): pass
    def setPixmap(self, *a): pass


class ImageLoader(QObject):
    """Centralized image loader with memory and disk caching"""

    # Signal emitted when image is loaded (for testing/monitoring)
    image_loaded = Signal(str, bool)  # url, success

    def __init__(self, cache_dir: str = None):
        super().__init__()
        self.network_manager = QNetworkAccessManager()
        self.memory_cache = {}  # {url_hash: QPixmap}

        # Set up cache directory
        if cache_dir is None:
            self.cache_dir = _get_writable_cache_dir()
        else:
            self.cache_dir = Path(cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Track active downloads to prevent duplicates
        self.active_downloads = {}  # {url: [callbacks]}

    # ✅ Fix 1: Single hash function — no more computing SHA256 twice
    def _get_hash(self, url: str) -> str:
        """Compute SHA256 hash of URL — single source of truth."""
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    def _get_cache_path(self, url: str) -> Path:
        """Return filesystem path for cached image based on URL hash."""
        return self.cache_dir / f"{self._get_hash(url)}.webp"  # ✅ Fix 2: WebP extension

    def _get_cache_key(self, url: str) -> str:
        """Generate cache key from URL."""
        return self._get_hash(url)  # ✅ Fix 1: delegates to _get_hash

    def load_image(self, url: str, label, width: int, height: int,
                   placeholder: str = "Loading...", error_text: str = "⚠️ Error"):
        """
        Asynchronously load an image from URL with caching.

        Args:
            url: Image URL
            label: QLabel to display the image
            width: Target width for scaled image
            height: Target height for scaled image
            placeholder: Text to show while loading
            error_text: Text to show on error
        """
        if not url or not url.strip():
            label.setText("N/A")
            label.setAlignment(Qt.AlignCenter)
            return

        url = url.strip()
        cache_key = self._get_hash(url)   # ✅ Fix 1: one call only
        cache_path = self._get_cache_path(url)

        # 1️⃣ Check memory cache
        if cache_key in self.memory_cache:
            self._set_label_pixmap(label, self.memory_cache[cache_key], width, height)
            return

        # 2️⃣ Check disk cache
        if cache_path.exists():
            pixmap = QPixmap(str(cache_path))
            if not pixmap.isNull():
                self.memory_cache[cache_key] = pixmap
                self._set_label_pixmap(label, pixmap, width, height)
                self.image_loaded.emit(url, True)
                return

        # 3️⃣ Download from network
        self._download_image(url, cache_key, cache_path, label, width, height,
                             placeholder, error_text)

    def prefetch(self, url: str):
        """Download and cache image in the background without displaying it."""
        if not url or not url.strip():
            return
        url = url.strip()
        cache_key = self._get_hash(url)   # ✅ Fix 1: one call only
        cache_path = self._get_cache_path(url)

        # Already cached → skip
        if cache_key in self.memory_cache or cache_path.exists():
            return

        self._download_image(url, cache_key, cache_path,
                             _DummyLabel(), 140, 190, "", "")

    def _download_image(self, url: str, cache_key: str, cache_path: Path,
                        label, width: int, height: int,
                        placeholder: str, error_text: str):
        """Handle network download of image"""

        # Check if already downloading this URL
        if url in self.active_downloads:
            self.active_downloads[url].append((label, width, height))
            return

        # Initialize callback list for this URL
        self.active_downloads[url] = [(label, width, height)]

        # Show loading state
        label.setText(placeholder)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: gray; font-size: 10px; background-color: #222;")

        # Validate URL
        q_url = QUrl(url)
        if not q_url.isValid():
            label.setText("❌ Invalid URL")
            self._cleanup_download(url)
            return

        # Create network request
        request = QNetworkRequest(q_url)
        request.setRawHeader(b"User-Agent", b"Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        request.setAttribute(
            QNetworkRequest.Attribute.RedirectPolicyAttribute,
            QNetworkRequest.RedirectPolicy.NoLessSafeRedirectPolicy
        )

        # Set timeout (10 seconds)
        request.setTransferTimeout(10000)

        # Start download
        reply = self.network_manager.get(request)

        def on_finished():
            callbacks = self.active_downloads.get(url, [])

            if reply.error() != QNetworkReply.NetworkError.NoError:
                error_msg = reply.errorString()
                print(f"Error loading image from {url}: {error_msg}")

                for cb_label, _, _ in callbacks:
                    cb_label.setText(error_text)
                    cb_label.setAlignment(Qt.AlignCenter)

                self.image_loaded.emit(url, False)
                self._cleanup_download(url)
                reply.deleteLater()
                return

            # Read image data
            data = reply.readAll()
            pixmap = QPixmap()

            if pixmap.loadFromData(data):
                # Cache in memory
                self.memory_cache[cache_key] = pixmap

                # Save to disk as WebP (25-35% smaller than JPG at same quality)
                try:
                    pixmap.save(str(cache_path), "WEBP", quality=85)  # ✅ Fix 2: WebP format
                    self._evict_if_over_limit(max_size_mb=50.0)
                except Exception as e:
                    print(f"Failed to save image to disk: {e}")

                # Update all waiting labels
                for cb_label, cb_width, cb_height in callbacks:
                    self._set_label_pixmap(cb_label, pixmap, cb_width, cb_height)

                self.image_loaded.emit(url, True)
            else:
                print(f"Failed to decode image data from {url}")

                for cb_label, _, _ in callbacks:
                    cb_label.setText(error_text)
                    cb_label.setAlignment(Qt.AlignCenter)

                self.image_loaded.emit(url, False)

            self._cleanup_download(url)
            reply.deleteLater()

        reply.finished.connect(on_finished)

    def _set_label_pixmap(self, label, pixmap: QPixmap, width: int, height: int):
        """Scale and set pixmap on label"""
        scaled_pixmap = pixmap.scaled(
            width, height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("")  # Clear loading style

    def _cleanup_download(self, url: str):
        """Remove URL from active downloads"""
        if url in self.active_downloads:
            del self.active_downloads[url]

    def clear_memory_cache(self):
        """Clear in-memory cache (useful for memory management)"""
        self.memory_cache.clear()

    def clear_disk_cache(self):
        """Clear disk cache (removes all cached images)"""
        for file in self.cache_dir.glob("*.webp"):  # ✅ Fix 2: WebP glob
            try:
                file.unlink()
            except Exception as e:
                print(f"Failed to delete {file}: {e}")

    def get_cache_size(self) -> dict:
        """Get cache statistics"""
        disk_files = list(self.cache_dir.glob("*.webp"))  # ✅ Fix 2: WebP glob
        disk_size = sum(f.stat().st_size for f in disk_files)

        return {
            "memory_images": len(self.memory_cache),
            "disk_images": len(disk_files),
            "disk_size_mb": disk_size / (1024 * 1024)
        }

    def _evict_if_over_limit(self, max_size_mb: float = 50.0):
        """Delete oldest cached files if total disk cache exceeds max_size_mb."""
        files = list(self.cache_dir.glob("*.webp"))  # ✅ Fix 2: WebP glob
        total_size = sum(f.stat().st_size for f in files)
        max_bytes = max_size_mb * 1024 * 1024

        if total_size <= max_bytes:
            return

        # Sort by oldest access time first
        files.sort(key=lambda f: f.stat().st_atime)

        for file in files:
            if total_size <= max_bytes:
                break
            try:
                total_size -= file.stat().st_size
                file.unlink()
                self.memory_cache.pop(file.stem, None)
            except Exception as e:
                print(f"Failed to evict {file}: {e}")


# ------------------------------------------------------------------
# 🌐 Global instance (singleton pattern)
# ------------------------------------------------------------------
_global_image_loader = None

def get_image_loader() -> ImageLoader:
    """Get or create the global ImageLoader instance"""
    global _global_image_loader
    if _global_image_loader is None:
        _global_image_loader = ImageLoader()
    return _global_image_loader


# ------------------------------------------------------------------
# 🔄 Backward-compatible function (deprecated)
# ------------------------------------------------------------------
def link_to_image(path: str, label, x: int, y: int):
    """
    Legacy function for backward compatibility.
    DEPRECATED: Use get_image_loader().load_image() instead.
    """
    loader = get_image_loader()
    loader.load_image(path, label, x, y)


def get_pixmap(url: str) -> QPixmap | None:
    """
    Delegate-safe function.
    Returns cached QPixmap or None.
    NEVER downloads.
    NEVER blocks.
    """
    if not url:
        return None

    loader = get_image_loader()
    cache_key = loader._get_hash(url)     # ✅ Fix 1: one call only
    cache_path = loader._get_cache_path(url)

    # 1️⃣ Memory cache (FASTEST)
    if cache_key in loader.memory_cache:
        return loader.memory_cache[cache_key]

    # 2️⃣ Disk cache (OK)
    if cache_path.exists():
        pixmap = QPixmap(str(cache_path))
        if not pixmap.isNull():
            loader.memory_cache[cache_key] = pixmap
            return pixmap

    # ❌ Not cached → delegate must NOT download
    return None