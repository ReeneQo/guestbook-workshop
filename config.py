"""Единая точка конфигурации приложения.

Все настройки читаются из переменных окружения (и из .env локально)
через pydantic-settings. В коде больше нет зашитых адресов и паролей.
"""

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Параметры PostgreSQL. Имена совпадают с переменными официального
    # образа postgres (POSTGRES_USER/PASSWORD/DB), поэтому в compose один и
    # тот же секрет можно отдать и базе, и приложению.
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    greeting: str = "Добро пожаловать в гостевую книгу!"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """Строка подключения собирается из частей — целиком её нигде не хранят."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


# Один общий экземпляр на всё приложение (читаем окружение один раз).
settings = Settings()  # type: ignore[call-arg]
