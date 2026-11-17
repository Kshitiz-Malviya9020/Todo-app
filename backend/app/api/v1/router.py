from fastapi import APIRouter
from app.api.v1.health import router as health_router

api_router = APIRouter()

#including heath routers in router module 
api_router.include_router(health_router)
