import os

from dynaconf import Dynaconf
from loguru import logger

# Инициализация настроек
class Settings(Dynaconf):

    @property
    def DB_URL(self):

        if self.current_env == "testing":
            logger.info(f"Запуск тестовой DB_URL")
            logger.info(f"current_env = {self.current_env}")
            return (
                f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
                f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
            )
        logger.info(f"Запуск обычной DB_URL")
        logger.info(f"current_env = {self.current_env}")
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def CELERY_DB_URL(self):
        if self.current_env == "testing":
            return (
                f"db+postgresql://{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
                f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
            )
        return (
            f"db+postgresql://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def RABBITMQ_URL(self):
        if self.current_env == "testing":
            return (
                f"pyamqp://{self.TEST_RABBITMQ_USER}:{self.TEST_RABBITMQ_PASS}"
                f"@{self.TEST_RABBITMQ_HOST}:{self.TEST_RABBITMQ_PORT}"
            )
        return (
            f"pyamqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"
        )

    @property
    def REDIS_URL(self):
        if self.current_env == "testing":
            return f"redis://{self.TEST_REDIS_HOST}:{self.TEST_REDIS_PORT}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


logger.info(f"ENV_FOR_DYNACONF перед инициализацией: {os.getenv('ENV_FOR_DYNACONF')}")

# Создаём объект настроек
settings = Settings(
    settings_files=["settings.dev.toml", ".secrets.toml"],
    environments=True,  # Поддержка окружений (development, production и т.д.)
)

logger.info(f"ENV_FOR_DYNACONF после инициализации: {os.getenv('ENV_FOR_DYNACONF')}")
logger.info(f"current_env после инициализации: {settings.current_env}")
