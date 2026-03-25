from qasync import asyncSlot


class RegesterPresenter:
    """Handles all auth business logic — signup, login, verify, resend"""

    def __init__(self, view, api_client):
        self.view = view
        self.api = api_client
        self._pending_email = None  # holds email between signup and verify steps

        self._connect_signals()

    # ── Signal wiring ───────────────────────────────────────────────────────
    def _connect_signals(self):
        ui = self.view.ui

        # Page switches
        ui.login_switchBtn.clicked.connect(self.view.show_login_page)
        ui.sign_up_switchBtn.clicked.connect(self.view.show_signup_page)
        ui.verify_back.clicked.connect(self._on_verify_back)

        # Actions
        ui.sign_up_button.clicked.connect(self._on_signup)
        ui.login_button.clicked.connect(self._on_login)
        ui.verify_button.clicked.connect(self._on_verify)
        ui.verify_resend.clicked.connect(self._on_resend)

    # ── Handlers ────────────────────────────────────────────────────────────
    @asyncSlot()
    async def _on_signup(self):
        fields = self.view.get_signup_fields()

        if not all(fields.values()):
            self.view.show_error("Please fill in all fields.")
            return

        self.view.set_signup_loading(True)
        try:
            result = await self.api.register(
                username=fields["username"],   # API schema: UserCreate.username
                email=fields["email"],
                password=fields["password"],
            )
            if result.ok:
                self._pending_email = fields["email"]
                self.view.clear_signup_fields()
                self.view.show_verify_page(self._pending_email)
            else:
                # Try to surface a readable message from the API error body
                message = self._extract_error(result.error) or "Registration failed."
                self.view.show_error(message)
        except Exception as e:
            self.view.show_error(f"Network error: {e}")
        finally:
            self.view.set_signup_loading(False)

    @asyncSlot()
    async def _on_login(self):
        fields = self.view.get_login_fields()

        if not all(fields.values()):
            self.view.show_error("Please enter your email and password.")
            return

        self.view.set_login_loading(True)
        try:
            result = await self.api.login(
                email=fields["email"],
                password=fields["password"],
            )
            if result.ok:
                self.view.clear_login_fields()
                self.view.login_success.emit()  # AppController takes over
            else:
                message = self._extract_error(result.error) or "Login failed."
                self.view.show_error(message)
        except Exception as e:
            self.view.show_error(f"Network error: {e}")
        finally:
            self.view.set_login_loading(False)

    @asyncSlot()
    async def _on_verify(self):
        code = self.view.get_verify_code()

        if not code:
            self.view.show_error("Please enter the verification code.")
            return

        self.view.set_verify_loading(True)
        try:
            result = await self.api.verify_email(
                email=self._pending_email,
                code=code,                     # API schema: VerifyEmail.code (6-digit str)
            )
            if result.ok:
                self.view.clear_verify_field()
                self.view.show_info("Email verified! You can now log in.")
                self.view.show_login_page()
            else:
                message = self._extract_error(result.error) or "Invalid code."
                self.view.show_error(message)
        except Exception as e:
            self.view.show_error(f"Network error: {e}")
        finally:
            self.view.set_verify_loading(False)

    @asyncSlot()
    async def _on_resend(self):
        if not self._pending_email:
            return

        self.view.set_verify_loading(True)
        try:
            result = await self.api.resend_verification(email=self._pending_email)
            if result.ok:
                self.view.show_info("A new code has been sent.")
            else:
                message = self._extract_error(result.error) or "Could not resend code."
                self.view.show_error(message)
        except Exception as e:
            self.view.show_error(f"Network error: {e}")
        finally:
            self.view.set_verify_loading(False)

    def _on_verify_back(self):
        self.view.clear_verify_field()
        self._pending_email = None
        self.view.show_signup_page()

    # ── Helpers ─────────────────────────────────────────────────────────────
    @staticmethod
    def _extract_error(raw: str | None) -> str | None:
        """
        Try to pull a human-readable message out of the raw API error text.
        Falls back to the raw string if JSON parsing fails.
        """
        if not raw:
            return None
        try:
            import json
            body = json.loads(raw)
            # FastAPI validation errors: {"detail": [{"msg": "..."}]}
            detail = body.get("detail")
            if isinstance(detail, list) and detail:
                return detail[0].get("msg", raw)
            if isinstance(detail, str):
                return detail
        except Exception:
            pass
        return raw