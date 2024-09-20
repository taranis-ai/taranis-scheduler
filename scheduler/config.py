from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APPLICATION_ROOT: str = "/scheduler"
    MODULE_ID: str = "Scheduler"
    DEBUG: bool = False

    JWT_IDENTITY_CLAIM: str = "sub"
    JWT_ACCESS_TOKEN_EXPIRES: int = 14400
    JWT_TOKEN_LOCATION: list = ["headers", "cookies"]
    JWT_ACCESS_COOKIE_NAME: str = "access_token_cookie"
    COLORED_LOGS: bool = True
    BUILD_DATE: datetime = datetime.now()
    GIT_INFO: dict[str, str] | None = None
    CACHE_TYPE: str = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT: int = 300
    TARANIS_CORE_URL: str = "http://taranis/api"
    SSL_VERIFICATION: bool = False
    REQUESTS_TIMEOUT: int = 60


Config = Settings()
