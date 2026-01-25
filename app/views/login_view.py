from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class AuthView(QWidget):
    """Pure UI component - no business logic"""
    
    # Signals for user actions
    signin_requested = Signal(str, str, str)  # name, email, password
    login_requested = Signal(str, str)  # email, password
    login_success = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Auth UI")
        self.setFixedSize(450, 600)
        self.setup_ui()

    def setup_ui(self):
        # Set modern dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                color: #eee;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                background-color: #16213e;
                border: 2px solid #0f3460;
                border-radius: 8px;
                padding: 12px;
                color: #eee;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #e94560;
            }
            QPushButton {
                background-color: #e94560;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d63447;
            }
            QPushButton:pressed {
                background-color: #c52a3a;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
            QPushButton#switchBtn {
                background-color: transparent;
                color: #e94560;
                text-decoration: underline;
                padding: 5px;
            }
            QPushButton#switchBtn:hover {
                color: #d63447;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Stacked widget to switch between sign in and login
        self.stacked_widget = QStackedWidget()
        
        # Create sign in page
        self.signin_page = self.create_signin_page()
        self.stacked_widget.addWidget(self.signin_page)
        
        # Create login page
        self.login_page = self.create_login_page()
        self.stacked_widget.addWidget(self.login_page)
        
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        
    def create_signin_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Create Account")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Sign up to get started")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #aaa;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Name input
        name_label = QLabel("Name")
        name_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        layout.addWidget(self.name_input)
        
        # Email input
        email_label = QLabel("Email")
        email_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(email_label)
        
        self.signin_email_input = QLineEdit()
        self.signin_email_input.setPlaceholderText("Enter your email")
        layout.addWidget(self.signin_email_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(password_label)
        
        self.signin_password_input = QLineEdit()
        self.signin_password_input.setPlaceholderText("Create a password")
        self.signin_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.signin_password_input)
        
        layout.addSpacing(10)
        
        # Sign in button
        self.signin_btn = QPushButton("Sign Up")
        self.signin_btn.clicked.connect(self._on_signin_clicked)
        layout.addWidget(self.signin_btn)
        
        # Switch to login
        switch_layout = QHBoxLayout()
        switch_layout.addStretch()
        switch_label = QLabel("Already have an account?")
        switch_label.setStyleSheet("color: #aaa;")
        switch_layout.addWidget(switch_label)
        
        switch_btn = QPushButton("Log In")
        switch_btn.setObjectName("switchBtn")
        switch_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        switch_layout.addWidget(switch_btn)
        switch_layout.addStretch()
        
        layout.addSpacing(10)
        layout.addLayout(switch_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
        
    def create_login_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Welcome Back")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Log in to your account")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #aaa;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Email input
        email_label = QLabel("Email")
        email_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(email_label)
        
        self.login_email_input = QLineEdit()
        self.login_email_input.setPlaceholderText("Enter your email")
        layout.addWidget(self.login_email_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(password_label)
        
        self.login_password_input = QLineEdit()
        self.login_password_input.setPlaceholderText("Enter your password")
        self.login_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password_input)
        
        layout.addSpacing(10)
        
        # Login button
        self.login_btn = QPushButton("Log In")
        self.login_btn.clicked.connect(self._on_login_clicked)
        layout.addWidget(self.login_btn)
        
        # Switch to sign in
        switch_layout = QHBoxLayout()
        switch_layout.addStretch()
        switch_label = QLabel("Don't have an account?")
        switch_label.setStyleSheet("color: #aaa;")
        switch_layout.addWidget(switch_label)
        
        switch_btn = QPushButton("Sign Up")
        switch_btn.setObjectName("switchBtn")
        switch_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        switch_layout.addWidget(switch_btn)
        switch_layout.addStretch()
        
        layout.addSpacing(10)
        layout.addLayout(switch_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    # UI-only methods - just emit signals or validate input
    def _on_signin_clicked(self):
        """Collect data and emit signal"""
        name = self.name_input.text().strip()
        email = self.signin_email_input.text().strip()
        password = self.signin_password_input.text()
        
        # Basic validation
        if not name or not email or not password:
            self.show_error("Please fill in all fields")
            return
        
        # Emit signal - let presenter handle the logic
        self.signin_requested.emit(name, email, password)
    
    def _on_login_clicked(self):
        """Collect data and emit signal"""
        email = self.login_email_input.text().strip()
        password = self.login_password_input.text()
        
        # Basic validation
        if not email or not password:
            self.show_error("Please fill in all fields")
            return
        
        # Emit signal - let presenter handle the logic
        self.login_requested.emit(email, password)
    
    # Public methods for presenter to control the view
    def set_ui_enabled(self, enabled: bool):
        """Enable/disable UI elements during async operations"""
        self.name_input.setEnabled(enabled)
        self.signin_email_input.setEnabled(enabled)
        self.signin_password_input.setEnabled(enabled)
        self.login_email_input.setEnabled(enabled)
        self.login_password_input.setEnabled(enabled)
        self.signin_btn.setEnabled(enabled)
        self.login_btn.setEnabled(enabled)
        
        if not enabled:
            self.signin_btn.setText("Processing...")
            self.login_btn.setText("Processing...")
        else:
            self.signin_btn.setText("Sign Up")
            self.login_btn.setText("Log In")
    
    def show_error(self, message: str):
        """Display error message"""
        QMessageBox.warning(self, "Error", message)
    
    def show_critical_error(self, message: str):
        """Display critical error message"""
        QMessageBox.critical(self, "Error", message)
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.name_input.clear()
        self.signin_email_input.clear()
        self.signin_password_input.clear()
        self.login_email_input.clear()
        self.login_password_input.clear()