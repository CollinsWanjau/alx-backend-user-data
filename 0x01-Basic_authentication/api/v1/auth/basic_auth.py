#!/usr/bin/env python3
"""
This module defines a basic class hierachy
"""


from api.v1.auth.auth import Auth
import base64


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
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, userpasswd = decoded_base64_authorization_header.split(':')
        return (email, userpasswd)
