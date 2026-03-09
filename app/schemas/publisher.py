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
    full_name: str
    email: EmailStr
    website: str


class PublsherUpdate(BaseModel):
    # TODO: Allow full_name, website
    pass
