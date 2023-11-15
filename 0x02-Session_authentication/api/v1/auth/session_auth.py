#!/usr/bin/env python3
"""
This script defines the SessionAuth class, which is intended to serve as a new
authentication mechanism for a web application.
"""


import uuid
from api.v1.auth.auth import Auth


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

        if not isinstance('user_id', str):
            return None

        session_id = str(uuid.uuid4())

        if user_id in self.user_id_by_session_id:
            return self.user_id_by_session_id[session_id].append(user_id)
        else:
            self.user_id_by_session_id[session_id] = user_id

        return session_id
