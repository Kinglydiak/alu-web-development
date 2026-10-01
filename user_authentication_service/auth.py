#!/usr/bin/env python3
"""Auth module that handles the authentication logic of the service."""
import uuid
from typing import Optional

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> str:
    """Return a salted bcrypt hash of the given password as a string."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def _generate_uuid() -> str:
    """Return a string representation of a newly generated UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self) -> None:
        """Initialize a new Auth instance with its own DB connection."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password, raising
        ValueError if a user with that email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email, hashed)
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Return True if a user with the given email exists and the
        password matches its stored hash, otherwise return False.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        stored = user.hashed_password
        if isinstance(stored, str):
            stored = stored.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored)

    def create_session(self, email: str) -> Optional[str]:
        """Create a session for the user with the given email, store the
        new session id in the database and return it, or return None if
        no user matches the email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
