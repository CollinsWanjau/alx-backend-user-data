#!/usr/bin/env python3
"""
This module defines a basic class hierachy
"""


from api.v1.auth.auth import Auth


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
