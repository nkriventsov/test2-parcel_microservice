from fastapi import APIRouter
from src.api.v1 import router as v1_router
from src.api import healthcheck
from src.api import tasks

api_router = APIRouter()
api_router.include_router(v1_router)
api_router.include_router(healthcheck.healthcheck_router)

api_router.include_router(tasks.tasks_router)

