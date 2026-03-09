from uuid import UUID
from fastapi import APIRouter

from app.schemas.publisher import PublisherCreate, PublisherRead
from app.api.dependencies import PublisherServiceDep

router = APIRouter(
    prefix="/publisher",
    tags=["Publisher"],
)


@router.post("/register", response_model=PublisherRead)
async def register_publisher(
    publisher: PublisherCreate,
    service: PublisherServiceDep,
):
    return await service.add(publisher)


@router.post("/login")
async def login_publisher():
    pass


@router.get("/profile")
async def get_publisher_profile():
    # Public endpoint
    pass


@router.get("/logout")
async def logout_publisher():
    pass
