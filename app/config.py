# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения.
    Настройки читаются из переменных окружения.
    """
    # Для генерации: openssl rand -hex 32
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Pydantic v2-style: .env файлы и префиксы
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Создаем экземпляр настроек, который будет использоваться во всем приложении
settings = Settings()