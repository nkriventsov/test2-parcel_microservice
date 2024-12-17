from fastapi import APIRouter
from src.api.v1 import router as v1_router
from src.api import healthcheck
from src.api.v1.endpoints import fx_rate_upd

api_router = APIRouter()
api_router.include_router(v1_router)
api_router.include_router(healthcheck.healthcheck_router)

api_router.include_router(fx_rate_upd.fx_rate)

