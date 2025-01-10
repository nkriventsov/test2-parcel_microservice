from dynaconf import Dynaconf


# Инициализация настроек
class Settings(Dynaconf):

    @property
    def DB_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def CELERY_DB_URL(self):
        return (
            f"db+postgresql://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def RABBITMQ_URL(self):
        return (
            f"pyamqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"
        )

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


    @property
    def SYNC_DATABASE_URL(self):
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Создаём объект настроек
settings = Settings(
    settings_files=["settings.dev.toml", ".secrets.toml"],
    environments=True,  # Поддержка окружений (development, production и т.д.)
    envvar_prefix="PARCEL",  # Префикс для переменных окружения
)
