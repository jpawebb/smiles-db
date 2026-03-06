from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.schemas.discovery import DiscoveryCreate
from app.database.models import Discovery, Publisher
from app.services.base import BaseService


class DiscoveryService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(Discovery, session)

    async def get(self, id: UUID) -> Discovery | None:
        return await self._get(id)

    async def add(
        self, discovery_create: DiscoveryCreate, publisher: Publisher
    ) -> Discovery:
        new_discovery = Discovery(
            **discovery_create.model_dump(),
            publisher_id=publisher.id,
        )

        return await self._add(new_discovery)

    async def update(self):
        pass

    async def delete(self, id: UUID) -> None:
        await self._delete(await self.get(id))
