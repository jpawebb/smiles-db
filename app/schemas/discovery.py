from uuid import UUID
from pydantic import BaseModel
from app.database.models import SmilesStr


class BaseDiscovery(BaseModel):
    name: str
    smiles: SmilesStr


class DiscoveryCreate(BaseDiscovery):
    pass


class DiscoveryRead(BaseDiscovery):
    id: UUID
    molecular_weight: float
    publisher_id: UUID
