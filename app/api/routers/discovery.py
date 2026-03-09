from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import PublisherDep, DiscoveryServiceDep
from app.schemas.discovery import DiscoveryRead, DiscoveryCreate

router = APIRouter(
    prefix="/discovery",
    tags=["Discovery"],
)


@router.get("/")
async def get_discovery(id: UUID, _: PublisherDep, service: DiscoveryServiceDep):
    # TODO: Anyone can get a discovery
    discovery = await service.get(id)

    if discovery is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No discovery found with that ID.",
        )

    return discovery


@router.post("/", response_model=DiscoveryRead)
async def post_discovery(
    publisher: PublisherDep,
    discovery: DiscoveryCreate,
    service: DiscoveryServiceDep,
):
    # TODO: Only an authenticated publisher can post a discovery
    return await service.add(discovery, publisher)
