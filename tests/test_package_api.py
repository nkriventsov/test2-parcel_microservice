import pytest
from unittest.mock import AsyncMock


class TestPackageAPI:

    @pytest.mark.asyncio
    async def test_get_packages(self, test_client, monkeypatch, mock_list_packages_query):
        """Тест для получения списка посылок"""
        monkeypatch.setattr(
            "src.api.v1.endpoints.package_routes.list_packages_query", mock_list_packages_query
        )

        response = test_client.get(
            "/packages/my_packages",
            cookies={"session_id": "test_session_id"}
        )

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "Малый короб"

    @pytest.mark.asyncio
    async def test_get_package(self, test_client, monkeypatch, mock_get_package_query):
        """Тест для получения данных посылки"""
        monkeypatch.setattr(
            "src.api.v1.endpoints.package_routes.get_package_query", mock_get_package_query
        )

        response = test_client.get(
            "/packages/1",
            cookies={"session_id": "test_session_id"}
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Малый короб"

    @pytest.mark.parametrize(
        "redis_response, celery_task_result, expected_status, expected_response",
        [
            ({"rub_to_usd": "75.5"}, {"package_id": 1}, 200, {"status": "success", "package_id": 1}),
            ({}, {"package_id": 1}, 200, {"status": "success", "package_id": 1}),
            ({"rub_to_usd": "75.5"}, None, 500, {"detail": "Ошибка при регистрации посылки"}),  # Обновлено ожидание
        ],
    )
    @pytest.mark.asyncio
    async def test_create_package_success(
            self, test_client, monkeypatch, redis_response, celery_task_result, expected_status, expected_response
    ):
        # Мок RedisManager
        mock_redis_manager = AsyncMock()
        mock_redis_manager.get.side_effect = lambda key: redis_response.get(key)
        monkeypatch.setattr("src.infrastructure.connectors.redis_connector.RedisManager", lambda: mock_redis_manager)

        # Мок Celery задачи
        class MockTask:
            def get(self, timeout=None):
                if celery_task_result is None:
                    raise ValueError("Ошибка в результате выполнения задачи Celery.")
                return celery_task_result

        monkeypatch.setattr(
            "src.infrastructure.tasks.tasks.register_package_task.apply_async",
            lambda *args, **kwargs: MockTask(),
        )

        # Данные для запроса
        package_data = {
            "name": "Малый короб",
            "weight": 0.5,
            "type_id": 1,
            "content_value": 100,
        }

        # Отправка POST-запроса через TestClient
        response = test_client.post(
            "/packages",
            json=package_data,
            cookies={"session_id": "test_session_id"},
        )

        # Проверка статуса и содержимого ответа
        assert response.status_code == expected_status, f"Ответ: {response.text}"
        assert response.json() == expected_response


    @pytest.mark.asyncio
    async def test_create_package_missing_field(self, test_client, monkeypatch, mock_redis_manager):
        """Тест для создания посылки с отсутствующим обязательным полем"""
        monkeypatch.setattr(
            "src.infrastructure.connectors.redis_connector.RedisManager", lambda: mock_redis_manager
        )

        package_data = {
            "weight": 0.5,
            "type_id": 1,
            "content_value": 100,
        }  # Отсутствует поле "name"

        response = test_client.post("/packages", json=package_data)

        assert response.status_code == 422
        assert "name" in response.json()["detail"][0]["loc"]

    @pytest.mark.asyncio
    async def test_get_package_no_session(self, test_client):
        """Тест для получения данных посылки без session_id"""
        response = test_client.get("/packages/1")

        assert response.status_code == 401


    @pytest.mark.asyncio
    async def test_get_packages_no_session(self, test_client):
        """Тест для получения списка посылок без session_id"""
        response = test_client.get("/packages/my_packages")

        assert response.status_code == 401

