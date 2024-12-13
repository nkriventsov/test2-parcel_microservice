# from fastapi import APIRouter
# from src.infrastructure.tasks.tasks import calculate_costs
#
#
# tasks_router = APIRouter(prefix="/tasks", tags=["Задачи"])
#
#
# @tasks_router.post("/calculate-costs", summary="Запуск расчёта стоимости")
# async def trigger_calculate_costs():
#     calculate_costs.apply_async()
#     return {"status": "Запущено"}

from fastapi import APIRouter
from src.core.celery_app import celery_instance

tasks_router = APIRouter(prefix="/tasks", tags=["Задачи"])


@tasks_router.post("/calculate-costs", summary="Запуск расчёта стоимости")
async def trigger_calculate_costs():
    # Отправляем задачу через Celery
    celery_instance.send_task("src.infrastructure.tasks.celery_tasks.calculate_costs")
    return {"status": "Запущено"}
