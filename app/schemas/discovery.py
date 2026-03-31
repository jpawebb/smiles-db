from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.database.models import SmilesStr


class BaseDiscovery(BaseModel):
    name: str
    smiles: SmilesStr


class DiscoveryCreate(BaseDiscovery):
    pass


class DiscoveryRead(BaseDiscovery):
    id: UUID
    created_at: datetime
    molecular_weight: float
    publisher_id: UUID

    model_config = {"from_attributes": True}
