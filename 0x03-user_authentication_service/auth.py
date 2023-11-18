#!/usr/bin/env python3
""" Module to hash a password
"""

import bcrypt


def _hash_password(password: str) -> str:
    """
    Hash the input password using bcrypt with salt.

    :param password: The password to hash.
    :return: The salted hash of the password as bytes.
    """
    # Generate a salt and hash the password with the generated salt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
