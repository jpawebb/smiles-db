from typing import Annotated
from uuid import UUID

import jwt
from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.models import Publisher, RevokedToken

from app.database.session import get_session
from app.services.discovery import DiscoveryService
from app.services.publisher import PublisherService
from app.utils import decode_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]

bearer_scheme = HTTPBearer()


async def get_current_publisher(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: SessionDep,
) -> Publisher:

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jti = payload.get("jti")
    if jti is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: token missing 'jti'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    revoked = await session.scalar(select(RevokedToken).where(RevokedToken.jti == jti))

    if revoked is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    publisher_data = payload.get("publisher")
    if publisher_data is None or "id" not in publisher_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing publisher information",
            headers={"WWW-Authenticate": "Bearer"},
        )

    publisher_id = UUID(publisher_data["id"])
    publisher = await session.get(Publisher, publisher_id)

    if publisher is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Publisher not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return publisher


PublisherDep = Annotated[Publisher, Depends(get_current_publisher)]


# Get discovery service dep
def get_discovery_service(session: SessionDep):
    return DiscoveryService(
        session,
    )


def get_publisher_service(session: SessionDep):
    return PublisherService(session=session)


PublisherServiceDep = Annotated[
    PublisherService,
    Depends(get_publisher_service),
]


DiscoveryServiceDep = Annotated[DiscoveryService, Depends(get_discovery_service)]
