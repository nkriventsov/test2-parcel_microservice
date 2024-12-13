from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn


# чтобы main.py "видел" директорию "src"
sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.api import api_router
from src.infrastructure.middleware.session import add_session_id_to_cookie
from src.core.config import settings
from src.infrastructure.connectors.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager._redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()
    # При выключении/перезагрузке приложения

app = FastAPI(title="Delivery Service API")

# Подключаем middleware
app.middleware("http")(add_session_id_to_cookie)

# Подключение маршрутов
app.include_router(api_router)

# Точка запуска приложения
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, workers=5)
    # uvicorn.run("main:app", host="0.0.0.0", port=settings.APP_PORT, reload=True, workers=5)
