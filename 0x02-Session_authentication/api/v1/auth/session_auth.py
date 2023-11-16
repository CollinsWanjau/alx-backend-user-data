#!/usr/bin/env python3
"""
This script defines the SessionAuth class, which is intended to serve as a new
authentication mechanism for a web application.
"""


import uuid
from api.v1.auth.auth import Auth
from api.v1.views.users import User


class SessionAuth(Auth):
    """
    SessionAuth class for a new authentication mechanism.
    Inherits from the Auth class.Thats all.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a given user_id.

        Args:
            user_id: The user identifier.
        Returns:
            The generated Session ID.
            Returns None if user_id is None or not a string.
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        if user_id in self.user_id_by_session_id:
            return self.user_id_by_session_id[session_id].append(user_id)
        else:
            self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Return User ID based on a given Session ID.

        Args:
            session_id: The Session ID.
        Return:
            The User ID associated with the Session ID.
            Returns None if session_id is None or not a string.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> User:
        """
        """
        # Return the session cookie value
        session_cookie_value = self.session_cookie(request)

        if session_cookie_value is None:
            return None

        # Retrieve the User ID based on the session cookie value
        user_id = self.user_id_for_session_id(session_cookie_value)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Delete the user session/logout.

        If the request is equal to None, return False.
        If the request doesnt contain the Session ID cookie, return False.
        If the Session ID of the request is not linked to any User ID,
        return False.
        Otherwise, delete in self.user_id_by_session_id the Session ID (as
        key of this dictionary) and return True.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
