import keyring

APP_NAME = "MyLibraryApp"  # This is the "Service Name" in the Keychain

def save_refresh_token(token_string):
    """Saves the refresh token securely in the OS Keychain."""
    # We use 'session_user' as a placeholder username
    keyring.set_password(APP_NAME, "refresh_token", token_string)

def get_refresh_token():
    """Retrieves the refresh token from the OS Keychain."""
    return keyring.get_password(APP_NAME, "refresh_token")

def delete_refresh_token():
    """Removes the token (used during Logout)."""
    try:
        keyring.delete_password(APP_NAME, "refresh_token")
    except keyring.errors.PasswordDeleteError:
        pass # Already deleted


