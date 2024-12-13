from fastapi import APIRouter
from src.api.v1.endpoints import package_routes, type_routes

router = APIRouter()
router.include_router(package_routes.router)
router.include_router(type_routes.router)
