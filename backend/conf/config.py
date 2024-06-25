from datetime import timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_HOST: str
    BIND_PORT: int
    DB_URL: str

    API_V1: str = "/api/v1"

    JWT_SECRET_SALT: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_CACHE_PREFIX: str
    FILE_EXPIRE_TIME: timedelta = timedelta(minutes=15)

    LOG_LEVEL: str = "debug"


settings = Settings()
