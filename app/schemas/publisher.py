from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PublisherCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    website: str | None = None


class PublisherRead(BaseModel):
    id: UUID
    created_at: datetime
    full_name: str | None = None
    email: EmailStr
    website: str | None = None

    model_config = {"from_attributes": True}


class PublisherUpdate(BaseModel):
    full_name: str | None = None
    website: str | None = None
