from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class Settings(BaseSettings):
    APP_NAME: str = "Todo API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Database configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "todo_db"
    DB_USER: str = "todo_user"
    DB_PASSWORD: SecretStr


settings = Settings()
