from fastapi import APIRouter
from src.infrastructure.tasks.tasks import update_exchange_rate_task


tasks_router = APIRouter(prefix="/tasks", tags=["Задачи"])


@tasks_router.post("/exchange-rate-update", summary="Загрузка курса USD")
async def trigger_fx_rate_update():
    update_exchange_rate_task.apply_async()
    return {"status": "Запущено"}
