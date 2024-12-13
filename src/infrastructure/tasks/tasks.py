from celery import shared_task
from src.domain.services.cost_calculator import calculate_delivery_cost
from src.infrastructure.external.currency_service import get_exchange_rate
from src.infrastructure.db.db_manager import DBManager
from src.infrastructure.db.database import async_session_maker


@shared_task
def calculate_costs():
    async def task_logic():
        async with async_session_maker() as session:
            db = DBManager(session)
            # Получаем необработанные посылки
            packages = await db.package.get_filtered(has_delivery_cost=False)
            exchange_rate = await get_exchange_rate(db.redis)

            for package in packages:
                cost = calculate_delivery_cost(package.weight, package.content_value, exchange_rate)
                await db.package.update(package.id, {"delivery_cost": cost})

            await db.commit()

    import asyncio
    asyncio.run(task_logic())

