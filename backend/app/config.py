from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DOMAIN: str = 'localhost'
    ENV: str = 'development'  # development | production

    DB_NAME: str = 'DB_NAME'
    DB_USER: str = 'DB_USER'
    DB_PASSWORD: str = 'DB_PASSWORD'
    DB_HOST: str = 'DB_HOST'
    DB_PORT: str = 'DB_PORT'

    JWT_SECRET: str = 'jwtsecret'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    COOKIE_DOMAIN: str = 'localhost'
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: str = 'lax'

    CORS_ORIGINS: str = 'https://localhost:5173,https://localhost:3000'

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
