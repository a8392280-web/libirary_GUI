from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from resources.py_ui.ui_regester import Ui_Form


class RegesterView(QWidget):
    """Pure View — only UI concerns, no business logic"""

    # Emitted when login succeeds (AppController listens to this)
    login_success = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    # ── Page switching ──────────────────────────────────────────────────────
    def show_signup_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.sign_up_page)

    def show_login_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)

    def show_verify_page(self, email: str):
        self.ui.verify_email_label.setText(email)
        self.ui.stackedWidget.setCurrentWidget(self.ui.verify_page)

    # ── Field readers ───────────────────────────────────────────────────────
    def get_signup_fields(self) -> dict:
        return {
            # Key renamed from "name" → "username" to match UserCreate API schema
            "username": self.ui.sign_up_name_line.text().strip(),
            "email":    self.ui.sign_up_email_line.text().strip(),
            "password": self.ui.sign_up_password_line.text(),
        }

    def get_login_fields(self) -> dict:
        return {
            "email":    self.ui.login_email.text().strip(),
            "password": self.ui.login_password.text(),
        }

    def get_verify_code(self) -> str:
        return self.ui.verify_code_line.text().strip()

    # ── UI state helpers ────────────────────────────────────────────────────
    def set_signup_loading(self, loading: bool):
        self.ui.sign_up_button.setEnabled(not loading)
        self.ui.sign_up_button.setText("Please wait…" if loading else "Sign up")

    def set_login_loading(self, loading: bool):
        self.ui.login_button.setEnabled(not loading)
        self.ui.login_button.setText("Please wait…" if loading else "Login")

    def set_verify_loading(self, loading: bool):
        self.ui.verify_button.setEnabled(not loading)
        self.ui.verify_resend.setEnabled(not loading)
        self.ui.verify_button.setText("Please wait…" if loading else "Verify")

    def clear_signup_fields(self):
        self.ui.sign_up_name_line.clear()
        self.ui.sign_up_email_line.clear()
        self.ui.sign_up_password_line.clear()

    def clear_login_fields(self):
        self.ui.login_email.clear()
        self.ui.login_password.clear()

    def clear_verify_field(self):
        self.ui.verify_code_line.clear()

    # ── Feedback ────────────────────────────────────────────────────────────
    def show_error(self, message: str):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message: str):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Info", message)