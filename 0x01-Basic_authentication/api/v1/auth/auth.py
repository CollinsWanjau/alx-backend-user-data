#!/usr/bin/env python3
"""
Module to manage the API authentication
"""


from flask import request
from typing import List, TypeVar


class Auth():
    """
    A class to manage the API authentication    
    """
        
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for a given path.

        Args:
            path (str): The path for which authentication is being checked.
            excluded_paths (List[str]): A list of paths that are excluded
            from authentication requirements.

        Returns:
            bool: True if authentication is required for the path, False if
            it's excluded.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Generate an authorization header for an HTTP request.

        Args:
            request (Optional[HttpRequest]): The HTTP request object.If not
            provided, it defaults to None.

        Returns:
            str: The authorization header as a string, or None if the request
            is not provided.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user based on the provided request.

        This function takes an optional 'request' parameter and returns an
        object of type 'User' representing the current user. If the 'request'
        parameter is not provided, it will return None.

        Returns:
            An object representing the current user or None if not found.

        Rtype:
            TypeVar('User')
        """
        return None
