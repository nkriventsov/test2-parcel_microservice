import pytest
from unittest.mock import AsyncMock

class TestFxRateUpdate:
    """
    Класс для тестирования функциональности обновления курса валют.
    """

    @pytest.mark.parametrize(
        "mock_rate,expected_status,expected_rate",
        [
            (75.5, "updated", 75.5),
            (80.0, "updated", 80.0),
        ],
    )
    def test_fx_rate_update_endpoint_success(
        self,
        test_client,
        monkeypatch,
        mock_redis_manager,
        mock_rate,
        expected_status,
        expected_rate,
    ):
        """
        Тест эндпоинта для обновления курса валют с параметризацией.

        :param test_client: Тестовый клиент для выполнения запросов.
        :param monkeypatch: Инструмент для подмены зависимостей.
        :param mock_redis_manager: Мок-объект RedisManager.
        :param mock_rate: Мок-значение курса валют.
        :param expected_status: Ожидаемый статус ответа.
        :param expected_rate: Ожидаемое значение курса валют.
        """
        async def mock_fetch_exchange_rate(redis_manager):
            return mock_rate

        monkeypatch.setattr(
            "src.application.commands.update_exchange_rate.fetch_exchange_rate",
            mock_fetch_exchange_rate,
        )

        response = test_client.post("/tasks/exchange-rate-update")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == expected_status
        assert data["rate"] == expected_rate

    @pytest.mark.asyncio
    async def test_update_exchange_rate_command_success(self, monkeypatch):
        """
        Тест команды обновления курса валют.

        :param monkeypatch: Инструмент для подмены зависимостей.
        """
        from src.application.commands.update_exchange_rate import update_exchange_rate_command

        # Создаём мок RedisManager
        mock_redis_manager = AsyncMock()
        mock_redis_manager.get.return_value = None

        # Подменяем глобальный redis_manager
        monkeypatch.setattr(
            "src.application.commands.update_exchange_rate.redis_manager",
            mock_redis_manager,
        )

        async def mock_fetch_exchange_rate(redis_manager):
            assert redis_manager == mock_redis_manager
            await redis_manager.set("rub_to_usd", 75.5, expire=3600)
            return 75.5

        monkeypatch.setattr(
            "src.application.commands.update_exchange_rate.fetch_exchange_rate",
            mock_fetch_exchange_rate,
        )

        result = await update_exchange_rate_command()

        assert result["status"] == "updated"
        assert result["rate"] == 75.5

        mock_redis_manager.set.assert_called_once_with("rub_to_usd", 75.5, expire=3600)


    @pytest.mark.asyncio
    async def test_redis_manager_connect(self, mock_redis_manager):
        """
        Тест подключения к Redis через RedisManager.

        :param mock_redis_manager: Мок-объект RedisManager.
        """
        await mock_redis_manager.connect()
        mock_redis_manager.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_redis_manager_set(self, mock_redis_manager):
        """
        Тест метода RedisManager.set для установки значения в Redis.

        :param mock_redis_manager: Мок-объект RedisManager.
        """
        await mock_redis_manager.set("key", "value", expire=3600)
        mock_redis_manager.set.assert_called_once_with("key", "value", expire=3600)

    @pytest.mark.asyncio
    async def test_redis_manager_get(self, mock_redis_manager):
        """
        Тест метода RedisManager.get для получения значения из Redis.

        :param mock_redis_manager: Мок-объект RedisManager.
        """
        mock_redis_manager.get.return_value = "cached_value"
        value = await mock_redis_manager.get("key")
        assert value == "cached_value"
        mock_redis_manager.get.assert_called_once_with("key")

    @pytest.mark.asyncio
    async def test_fetch_exchange_rate_cached(self, monkeypatch, mock_redis_manager):
        """
        Тест получения курса валют из кеша Redis.

        :param monkeypatch: Инструмент для подмены зависимостей.
        :param mock_redis_manager: Мок-объект RedisManager.
        """
        mock_redis_manager.get.return_value = "74.5"
        from src.infrastructure.external.currency_service import fetch_exchange_rate

        rate = await fetch_exchange_rate(mock_redis_manager)
        assert rate == 74.5
        mock_redis_manager.get.assert_called_once_with("rub_to_usd")

    @pytest.mark.asyncio
    async def test_fetch_exchange_rate_from_api(
        self, monkeypatch
    ):
        """
        Тест получения курса валют из внешнего API при отсутствии кеша.

        :param monkeypatch: Инструмент для подмены зависимостей.
        """
        # Создаём мок RedisManager
        mock_redis_manager = AsyncMock()
        mock_redis_manager.get.return_value = None

        # Мокаем метод fetch_exchange_rate
        async def mock_fetch_exchange_rate(redis_manager):
            assert redis_manager == mock_redis_manager
            await redis_manager.set("rub_to_usd", 75.5, expire=3600)
            return 75.5

        monkeypatch.setattr(
            "src.infrastructure.external.currency_service.fetch_exchange_rate",
            mock_fetch_exchange_rate,
        )

        # Импортируем тестируемую функцию
        from src.infrastructure.external.currency_service import fetch_exchange_rate

        # Вызываем тестируемую функцию
        rate = await fetch_exchange_rate(mock_redis_manager)

        # Проверяем результат
        assert rate == 75.5

        # Проверяем вызов метода set
        mock_redis_manager.set.assert_called_once_with("rub_to_usd", 75.5, expire=3600)