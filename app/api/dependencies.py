from typing import Annotated

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database.models import Publisher

from app.database.session import get_session
from app.services.discoveries import DiscoveryService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_publisher(session: SessionDep):
    stmt = select(Publisher).where(Publisher.email == "test@example.com")
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        publisher = Publisher(email="test@example.com", hashed_password="hashed_pw")
        session.add(publisher)
        await session.commit()
        await session.refresh(publisher)
        return publisher

    return await session.get(Publisher, user.id)


# Get discovery service dep
def get_discovery_service(session: SessionDep):
    return DiscoveryService(
        session,
    )


PublisherDep = Annotated[Publisher, Depends(get_current_publisher)]

DiscoveryServiceDep = Annotated[DiscoveryService, Depends(get_discovery_service)]
