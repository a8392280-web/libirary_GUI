from PySide6.QtCore import Qt, QTimer, QSize, QObject, QEvent
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


class LoadingSpinner(QWidget):
    def __init__(
        self,
        parent=None,
        radius=10,
        line_length=6,
        line_width=2,
        lines=12,
        color=QColor(220, 220, 220),
    ):
        super().__init__(parent)
        self._radius = radius
        self._line_length = line_length
        self._line_width = line_width
        self._lines = lines
        self._color = color
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.setInterval(50)
        self._timer.timeout.connect(self._rotate)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        size = (self._radius + self._line_length + self._line_width) * 2
        self.setFixedSize(QSize(size, size))
        self.hide()

    def start(self):
        if not self._timer.isActive():
            self._timer.start()
        self.show()

    def stop(self):
        self._timer.stop()
        self.hide()

    def _rotate(self):
        self._angle = (self._angle + (360 // self._lines)) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._angle)

        step = 360 / self._lines
        for i in range(self._lines):
            alpha = int(255 * (i + 1) / self._lines)
            color = QColor(self._color)
            color.setAlpha(alpha)
            painter.setPen(QPen(color, self._line_width, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(0, -self._radius, 0, -self._radius - self._line_length)
            painter.rotate(step)


class SpinnerOverlay(QObject):
    def __init__(self, target: QWidget, **spinner_kwargs):
        super().__init__(target)
        self._target = target
        self._host = target.viewport() if hasattr(target, "viewport") else target
        self._spinner = LoadingSpinner(self._host, **spinner_kwargs)

        self._center()
        self._target.installEventFilter(self)
        if self._host is not self._target:
            self._host.installEventFilter(self)

    def start(self):
        self._center()
        self._spinner.raise_()
        self._spinner.start()

    def stop(self):
        self._spinner.stop()

    def _center(self):
        host = self._host
        x = max(0, (host.width() - self._spinner.width()) // 2)
        y = max(0, (host.height() - self._spinner.height()) // 2)
        self._spinner.move(x, y)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize and obj in (self._target, self._host):
            self._center()
        return False
