from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from argon2 import PasswordHasher
from fastapi import HTTPException, status

from app.schemas.publisher import PublisherCreate
from app.database.models import Publisher
from app.services.base import BaseService
from app.utils import generate_access_token

ph = PasswordHasher()


class PublisherService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Publisher, session=session)

    async def add(self, publisher_create: PublisherCreate) -> Publisher:
        data = publisher_create.model_dump()

        raw_password = data.pop("password")

        new_publisher = Publisher(
            **data,
            hashed_password=ph.hash(raw_password),
        )

        return await self._add(new_publisher)

    async def _get_by_email(self, email: str) -> Publisher | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str:
        pub = await self._get_by_email(email)

        if pub is None or not ph.verify(pub.hashed_password, password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        # Already validated publisher
        return generate_access_token(
            data={
                "publisher": {
                    "name": pub.full_name,
                    "id": str(pub.id),
                }
            }
        )

    async def token(self, email, password) -> str:
        return await self._generate_token(email, password)
