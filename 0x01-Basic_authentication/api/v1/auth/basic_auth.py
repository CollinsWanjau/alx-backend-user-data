#!/usr/bin/env python3
"""
This module defines a basic class hierachy
"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    A subclass that inherits from Baseclass
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
            authorization_header: The Authorization header string.
        Returns:
            The Base64 part of the Authorization header or an empty string if
            conditions are not met.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        auth_parts = authorization_header.split(' ')[-1]
        return auth_parts

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 Authorization header.

        Args:
            base64_authorization_header: The Base64 Authorization header
            string.
        Returns:
            The decoded value or None if conditions are not met.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            data = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(data)
            return decoded.decode('utf-8')
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from the decoded Base64 Authorization
        header.

        Args:
            decoded_base64_authorization_header: The decoded Base64
            Authorization header string.
        Returns:
            A tuple containing user email and password or (None, None) if
            conditions are not met.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, userpasswd = decoded_base64_authorization_header.split(':')
        return (email, userpasswd)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        """
        if user_email is None or not isinstance("user_email", str):
            return None

        if user_pwd is None or not isinstance("user_pwd", str):
            return None
        user_name_db = User.search({'email': user_email})

        if not user_name_db:
            return None

        for user in user_name_db:
            if user.is_valid_password(user_pwd):
                return user

        return None
