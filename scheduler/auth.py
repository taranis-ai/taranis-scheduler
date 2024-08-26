from flask import Flask
import requests
from flask_jwt_extended import JWTManager
from scheduler.log import logger
from scheduler.config import Config

jwt = JWTManager()


def init(app: Flask):
    global jwt
    jwt.init_app(app)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    logger.debug(f"Validating user: {jwt_data}")
    logger.debug(f"Header data: {_jwt_header}")
    identity = jwt_data[Config.JWT_IDENTITY_CLAIM]
    if not identity:
        return None
    try:
        response = requests.get(f"{Config.TARANIS_CORE_URL}/users", headers={"Authorization": _jwt_header})
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
