from fastapi import APIRouter

from src.application.commands.update_exchange_rate import update_exchange_rate_command
from src.infrastructure.tasks.tasks import update_exchange_rate_task


fx_rate = APIRouter(prefix="/tasks", tags=["Задачи"])


@fx_rate.post("/exchange-rate-update", summary="Загрузка курса USD")
async def fx_rate_update():
    return await update_exchange_rate_command()