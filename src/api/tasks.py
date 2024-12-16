from fastapi import APIRouter
from src.infrastructure.tasks.tasks import update_exchange_rate_task


tasks_router = APIRouter(prefix="/tasks", tags=["Задачи"])


@tasks_router.post("/calculate-costs", summary="Запуск расчёта стоимости")
async def trigger_calculate_costs():
    update_exchange_rate_task.apply_async()
    return {"status": "Запущено"}
