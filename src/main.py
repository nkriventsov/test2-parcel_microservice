import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

import aiomonitor
import asyncio

# чтобы main.py "видел" директорию "src"
sys.path.append(str(Path(__file__).parent.parent))

from src.core.logger import logger
from src.api import api_router
from src.infrastructure.middleware.session import add_session_id_to_cookie


app = FastAPI(title="Delivery Service API")

# Подключаем middleware
app.middleware("http")(add_session_id_to_cookie)

# Подключение маршрутов
app.include_router(api_router)


# Точка запуска приложения
if __name__ == "__main__":
    # Создаем новый цикл событий
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    logger.debug("Инициализация aiomonitor...")
    # Запускаем мониторинг
    with aiomonitor.start_monitor(loop=loop, host="0.0.0.0", port=50102):
        logger.debug("aiomonitor запущен, передаем управление uvicorn.")
        # Передаем созданный цикл событий в uvicorn.run
        uvicorn.run("main:app", reload=True, workers=5)
        # uvicorn.run("main:app", host="0.0.0.0", port=settings.APP_PORT, reload=True, workers=5)
