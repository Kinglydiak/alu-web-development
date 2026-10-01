#!/usr/bin/env python3
"""Auth module that handles the authentication logic of the service."""
import bcrypt


def _hash_password(password: str) -> str:
    """Return a salted bcrypt hash of the given password as a string."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')
