from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_TTL: int = 60 * 24 * 8
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = 'HS256'
    WX_APP_ID: str = 'wx2fac3d97e10ca675'

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
