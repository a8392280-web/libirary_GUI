from PySide6.QtCore import QSettings


class AppSettings:
    def __init__(self):
        self._settings = QSettings("MyLib", "MyLibApp")

    def get_view_mode(self) -> str:
        return self._settings.value("view_mode", "grid")

    def set_view_mode(self, mode: str):
        if mode in ("grid", "list"):
            self._settings.setValue("view_mode", mode)
            self._settings.sync()

    def get_sort_index(self) -> int:
        value = self._settings.value("sort_index", 0)
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def set_sort_index(self, index: int):
        self._settings.setValue("sort_index", int(index))
        self._settings.sync()
