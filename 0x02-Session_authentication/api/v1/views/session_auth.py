#!/usr/bin/env python3
"""
Module of session auth
"""

import os
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    Handle user login using Session authentication.

    This route expects a POST request with 'email' and 'password' parameters
    in the form data.

    Returns:
        JSON representation of the User with a session cookie.
        Returns appropriate error responses if parameters are missing, the user
        is not found, the password is incorrect, or an unexpected error occurs.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    try:
        user_instance = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not user_instance:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_instance[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_cookie = os.environ.get('SESSION_NAME')
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())
    response.set_cookie(session_cookie, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Route: DELETE /api/v1/auth_session/logout

    Logout the user by destroying the session.
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
