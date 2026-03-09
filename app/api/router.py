from fastapi import APIRouter
from app.api.routers import discovery, publisher

master_router = APIRouter()

master_router.include_router(discovery.router)
master_router.include_router(publisher.router)
