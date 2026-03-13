# app/security/password.py
# This module provides functions for hashing and verifying passwords using bcrypt.
# It uses the passlib library, which is a popular choice for secure password hashing in Python.
# The functions defined here can be used in the authentication logic of the application to securely handle user passwords.
# Note: Ensure that the passlib library is installed in your environment (e.g., via pip install passlib) to use this module.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.
    Automatically truncates passwords to 72 bytes (bcrypt limit).
    """
    # Truncate the password safely to 72 bytes
    truncated = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed password.
    Also truncates to 72 bytes to avoid bcrypt errors.
    """
    truncated = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(truncated, hashed_password)
