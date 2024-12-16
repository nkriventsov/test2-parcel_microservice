from loguru import logger
import redis.asyncio as redis


class RedisManager:
    """Класс для управления подключением к Redis."""
    _redis: redis.Redis | None

    def __init__(self, host: str, port: int):
        """
        Инициализация RedisManager.
        :param host: Хост для подключения к Redis.
        :param port: Порт для подключения к Redis.
        """
        self.host = host
        self.port = port
        self._redis = None  # Объект Redis будет инициализирован в connect()

    async def connect(self):
        """Подключение к Redis."""
        logger.info(f"Начинаю подключение к Redis host={self.host}, port={self.port}")
        try:
            self._redis = redis.from_url(f"redis://{self.host}:{self.port}")
            # Проверяем соединение
            assert await self._redis.ping(), "Redis не доступен!"
            logger.info(f"Успешное подключение к Redis host={self.host}, port={self.port}")
        except Exception as e:
            logger.error(f"Ошибка подключения к Redis: {e}")
            raise

    async def _ensure_connected(self):
        """Проверка и повторное подключение к Redis при необходимости."""
        if self._redis is None or not await self._redis.ping():
            logger.warning("Соединение с Redis потеряно. Повторное подключение...")
            await self.connect()

    async def set(self, key: str, value: str, expire: int | None = None):
        """
        Установить значение в Redis.
        :param key: Ключ для сохранения значения.
        :param value: Значение для сохранения.
        :param expire: Время жизни ключа в секундах (опционально).
        """
        await self._ensure_connected()
        try:
            if expire:
                await self._redis.set(key, value, ex=expire)
            else:
                await self._redis.set(key, value)
            logger.info(f"Значение {value} сохранено в Redis с ключом {key}")
        except Exception as e:
            logger.error(f"Ошибка при записи в Redis: {e}")
            raise

    async def get(self, key: str):
        """
        Получить значение из Redis.
        :param key: Ключ для получения значения.
        :return: Значение, сохраненное по ключу, или None, если ключ не существует.
        """
        await self._ensure_connected()
        try:
            value = await self._redis.get(key)
            logger.info(f"Получено значение {value} для ключа {key} из Redis")
            return value
        except Exception as e:
            logger.error(f"Ошибка при чтении из Redis: {e}")
            raise

    async def delete(self, key: str):
        """
        Удалить ключ из Redis.
        :param key: Ключ для удаления.
        """
        await self._ensure_connected()
        try:
            await self._redis.delete(key)
            logger.info(f"Ключ {key} удалён из Redis")
        except Exception as e:
            logger.error(f"Ошибка при удалении из Redis: {e}")
            raise

    async def close(self):
        """Закрыть подключение к Redis."""
        if self._redis:
            try:
                await self._redis.close()
                logger.info("Подключение к Redis успешно закрыто.")
            except Exception as e:
                logger.error(f"Ошибка при закрытии подключения к Redis: {e}")
                raise

    async def __aenter__(self):
        """Подключение к Redis при входе в контекст."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрытие подключения к Redis при выходе из контекста."""
        await self.close()
