from uuid import uuid4
from fastapi import FastAPI, Request, Response
from loguru import logger

app = FastAPI()


@app.middleware("http")
async def add_session_id_to_cookie(request: Request, call_next):
    try:
        logger.info(f"Обработка запроса: {request.method} {request.url}")

        # Обрабатываем запрос через следующий слой middleware или конечную точку
        response: Response = await call_next(request)
        logger.debug("Ответ получен от следующего слоя")

        # Проверяем, есть ли session_id в cookies
        session_id = request.cookies.get("session_id")
        if not session_id:
            # Генерируем новый session_id
            session_id = str(uuid4())
            response.set_cookie(key="session_id", value=session_id, httponly=True)
            logger.info(f"Новый session_id создан: {session_id}")
        else:
            logger.debug(f"Существующий session_id найден: {session_id}")

        return response

    except Exception as e:
        logger.error(f"Ошибка в middleware add_session_id_to_cookie: {e}")
        raise