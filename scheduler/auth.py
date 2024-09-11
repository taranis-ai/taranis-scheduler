from flask import Flask, request
import requests
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from scheduler.log import logger
from scheduler.config import Config
from functools import wraps

jwt = JWTManager()


def init(app: Flask):
    global jwt
    jwt.init_app(app)


def jwt_auth(optional: bool = False):
    def auth_required_wrap(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            error = ({"error": "not authorized"}, 401)

            try:
                verify_jwt_in_request(optional=optional)
            except Exception as ex:
                logger.exception(str(ex))
                return error

            return fn(*args, **kwargs)

        return wrapper

    return auth_required_wrap


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # Extract the JWT cookie
    jwt_cookie = request.cookies.get(Config.JWT_ACCESS_COOKIE_NAME)
    if not jwt_cookie:
        logger.error("JWT cookie is missing")
        return None

    identity = jwt_data.get(Config.JWT_IDENTITY_CLAIM)
    if not identity:
        return None

    try:
        # Forward the JWT cookie to the core service
        cookies = {Config.JWT_ACCESS_COOKIE_NAME: jwt_cookie}
        response = requests.get(f"{Config.TARANIS_CORE_URL}/users", cookies=cookies)

        if not response.ok:
            logger.error(f"Error validating user: {identity} JWT with core service: {response.text}")
            return None

        return response.json()

    except requests.RequestException as e:
        logger.error(f"Error validating user: {identity} JWT with core service: {e}")
        return None



@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["username"]
