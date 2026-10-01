#!/usr/bin/env python3
"""DB module that handles the database connection and user storage."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class that manages the SQLite database and its sessions."""

    def __init__(self) -> None:
        """Initialize a new DB instance and create fresh tables."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Return a memoized session object used to talk to the database."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a user with the given email and hashed password, save it
        to the database and return the resulting User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Return the first user matching the given keyword arguments,
        raising NoResultFound if none match and InvalidRequestError if a
        keyword is not a valid User column.
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update the user identified by user_id with the given keyword
        arguments and commit, raising ValueError if a keyword does not
        correspond to a user attribute.
        """
        user = self.find_user_by(id=user_id)
        columns = User.__table__.columns.keys()
        for key in kwargs:
            if key not in columns:
                raise ValueError()
        for key, value in kwargs.items():
            setattr(user, key, value)
        self._session.commit()
