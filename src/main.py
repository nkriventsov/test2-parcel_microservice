import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

# чтобы main.py "видел" директорию "src"
sys.path.append(str(Path(__file__).parent.parent))


from src.api import api_router
from src.infrastructure.middleware.session import add_session_id_to_cookie


app = FastAPI(title="Delivery Service API")

# Подключаем middleware
app.middleware("http")(add_session_id_to_cookie)

# Подключение маршрутов
app.include_router(api_router)

# Подключение метрик для Prometheus
Instrumentator().instrument(app).expose(app)


# Точка запуска приложения
if __name__ == "__main__":
    # Для запуска в dev режиме
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

    # # Для запуска в prod режиме - прописано командой в docker-compose
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=5)
