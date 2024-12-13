from uuid import uuid4
from fastapi import FastAPI, Request, Response

app = FastAPI()


@app.middleware("http")
async def add_session_id_to_cookie(request: Request, call_next):
    response: Response = await call_next(request)

    # Проверяем, есть ли session_id в cookies
    session_id = request.cookies.get("session_id")
    if not session_id:
        # Генерируем новый session_id
        session_id = str(uuid4())
        response.set_cookie(key="session_id", value=session_id, httponly=True)

    return response
