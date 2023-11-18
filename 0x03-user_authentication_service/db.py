#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError


from user import Base, User
from typing import Dict, List


class DB:
    """ DB class

    This class provides database operations.

    Attributes:
        - _engine: Database engine
        - __session: Memoized database session
    Methods:
        - __init__: Initialize a new DB instance
        - add_user: Add a new user to the database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance

        This method initializes a new DB instance, creates the database tables
        if they don't exist, and sets up the database engine.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)

        # Drops all tables in the db if any
        Base.metadata.drop_all(self._engine)

        # Creates new tables based on the definitions in the base class
        Base.metadata.create_all(self._engine)

        self._session = None

    @property
    def _session(self) -> None:
        """Memoized session object

        This property returns a memoized session object. If the session does
        not exist, it creates a new one.

        Returns:
            Session: The database session object
        """
        if self.__session is None:
            # Used to create a new session factory that is bound to the engine
            # object created in __init__().The session factory is used to
            # create a new session object that can be used to execute sql
            # statements
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    # @_session.setter
    # def _session(self, value):
    #     self.__session = value

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        This method adds a new user to the database. It takes two required
        string arguments:email and hashed_password, and returns a User
        object representing the added user.

        Args:
            - email (str): Email of the user

        Returns:
            User: The User object representing the added user
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        # try:
        #     row = self._session.query(User).filter_by(**kwargs).first()
        #     if row is None:
        #         raise NoResultFound
        #     return row
        # except InvalidRequestError:
        #     raise InvalidRequestError
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user
