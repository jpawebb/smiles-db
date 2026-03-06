from fastapi import APIRouter
from app.api.routers import discovery

master_router = APIRouter()

master_router.include_router(discovery.router)
