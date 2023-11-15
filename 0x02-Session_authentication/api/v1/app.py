#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
#  configuring Cross-Origin Resource Sharing (CORS). This configuration allows
#  any domain to access resources under the "/api/v1/" route.
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
# Read the AUTH_TYPE environment variable
auth_type = os.environ.get('AUTH_TYPE')

# create an instance of Auth based on the AUTH_TYPE
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def before_request():
    """
    This function is a before_request handler in a web application using Flask.
    It is used to perform certain checks before handling incoming requests.

    Before each incoming request, this function checks if authentication (auth)
    is available. If auth is not available, it does nothing. If auth is
    available, it proceeds to check the request path against a list of
    exception paths. If the request path is not in the exception list, it
    performs further authentication checks.

    Raises:
        401: If the request path is not in the exception list and no valid
        authorization header is provided, it aborts the request with a 401
        error (unauthorized).
    """
    if auth is None:
        pass
    else:
        exception_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                           '/api/v1/forbidden/', '/api/v1/auth_session/login/']

        if auth.require_auth(request.path, exception_paths):
            authorization_header = auth.authorization_header(request)
            cookie = auth.session_cookie(request)
            if authorization_header or cookie is None:
                abort(401, description='unauthorized')
            current_user = auth.current_user(request)
            if current_user is None:
                abort(403, description='Forbidden')


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        str: _description_
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handle 403 Forbidden errors and return a JSON response.

    Args:
        error (Exception): The exception raised for the Forbidden error.

    Returns:
        Tuple[str, int]: A tuple containing a JSON response and HTTP status
        code (403).
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
