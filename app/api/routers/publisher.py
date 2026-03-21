import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import select

from app.schemas.publisher import PublisherCreate, PublisherRead
from app.schemas.auth import TokenResponse, LoginRequest
from app.api.dependencies import (
    PublisherDep,
    PublisherServiceDep,
    SessionDep,
    bearer_scheme,
)
from app.database.models import RevokedToken
from app.utils import decode_access_token

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


@router.post("/login", response_model=TokenResponse)
async def login_publisher(body: LoginRequest, service: PublisherServiceDep):
    """Authenticate a publisher and return a JWT"""
    token = await service.token(body.email, body.password)
    return TokenResponse(access_token=token)


@router.get("/profile", response_model=PublisherRead)
async def get_publisher_profile(publisher: PublisherDep):
    """Get authenticated publisher's profile"""
    return publisher


@router.get("/logout")
async def logout_publisher(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: SessionDep = None,
):
    """Revoke the current JWT access token to log out the publisher"""

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    jti = payload.get("jti")
    if jti is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing jti",
        )

    existing = await session.scalar(select(RevokedToken).where(RevokedToken.jti == jti))
    if existing is None:
        revoked = RevokedToken(jti=jti)
        session.add(revoked)
        await session.commit()
    return {"detail": "Token revoked, logged out successfully"}
