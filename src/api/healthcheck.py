from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from loguru import logger

from src.core.config import settings
from src.infrastructure.dependencies import DBDep
from src.domain.models.package import PackageOrm
from src.infrastructure.connectors.redis_connector import RedisManager
from src.core.celery_app import celery_instance

from src.exceptions import DatabaseConnectionHTTPException, DatabaseConnectionException


healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["Проверка состояния"],
)


@healthcheck_router.get(
    "/",
    summary="Healthcheck",
    description="Проверка состояния приложения",
    response_model=dict,
)
async def healthcheck(db: DBDep):
    try:
        # 1. Проверка подключения к базе данных
        logger.info("Проверка подключения к базе данных...")
        await db.session.execute(select(PackageOrm).limit(1))
        logger.success("Подключение к базе данных успешно!")

        # 2. Проверка подключения к Redis
        logger.info("Проверка подключения к Redis...")
        redis_manager = RedisManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        try:
            # Подключение и ping Redis
            await redis_manager.connect()
            logger.success("Соединение с Redis установлено.")
        except Exception as e:
            logger.error(f"Ошибка при подключении к Redis: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Redis не доступен."
            )
        finally:
            await redis_manager.close()

        # 3. Проверка подключения к RabbitMQ
        logger.info("Проверка подключения к RabbitMQ...")
        try:
            inspect = celery_instance.control.inspect()
            workers = inspect.ping()
            if not workers:
                logger.error("RabbitMQ не имеет активных worker-ов.")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="RabbitMQ не доступен или нет активных worker-ов.",
                )
            logger.success("Подключение к RabbitMQ успешно!")
        except Exception as e:
            logger.error(f"Ошибка при проверке RabbitMQ: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RabbitMQ не доступен.",
            )

        return {"status": "Ok"}

    except DatabaseConnectionException:
        logger.error("Подключение к базе данных не удалось.")
        raise DatabaseConnectionHTTPException

    except Exception as e:
        logger.error(f"Ошибка при выполнении healthcheck: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при выполнении healthcheck.",
        )

