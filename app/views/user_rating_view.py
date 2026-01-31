from resources.py_ui.ui_user_rating_ui import Ui_Form
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal


class UserRatingView(QDialog):
    """Pure UI component for user rating dialog"""
    rating_changed = Signal(float)  # Emit new rating
    def __init__(self, current_rating: int, parent=None):
        super().__init__()
        # Setup UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)


        self.ui.label.setText(str(int(current_rating)))
        self.ui.horizontalSlider.setValue(int(current_rating))
        self.ui.buttonBox.accepted.connect(self._on_accepted)
        self.ui.buttonBox.rejected.connect(self.reject)

    def _on_accepted(self):
        """Emit rating when OK is clicked"""
        rating = self.ui.horizontalSlider.value()
        self.rating_changed.emit(rating)
        self.accept()

    def get_rating(self):
        return self.ui.horizontalSlider.value()

