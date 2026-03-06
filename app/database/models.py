from typing import Annotated
from pydantic import AfterValidator, field_validator
from uuid import uuid4, UUID
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

from rdkit import Chem
from rdkit.Chem import Descriptors

from app.utils import validate_smiles

SmilesStr = Annotated[str, AfterValidator(validate_smiles)]


class BaseIDModel(SQLModel, table=False):

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_on: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )


class User(BaseIDModel, table=True):
    __tablename__ = "users"

    type: str = Field(
        default="user",
        sa_column_kwargs={"index": True},
    )

    email: str
    hashed_password: str = Field(nullable=False)
    full_name: str | None = Field(default=None)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
    }


class Publisher(User, table=True):
    __tablename__ = "publishers"

    id: UUID = Field(
        foreign_key="users.id",
        primary_key=True,
    )

    website: str = Field(default=None)

    __mapper_args__ = {"polymorphic_identity": "publisher"}

    discoveries: list["Discovery"] = Relationship(
        back_populates="publisher",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# Discovery entities
class Discovery(BaseIDModel, table=True):
    __tablename__ = "discoveries"

    name: str
    smiles: SmilesStr = Field(index=True, unique=True, nullable=False)
    molecular_weight: float = Field(default=0.0, index=True)

    publisher_id: UUID = Field(foreign_key="users.id", nullable=False)

    publisher: "Publisher" = Relationship(back_populates="discoveries")

    @field_validator("molecular_weight")
    @classmethod
    def calculate_mw(cls, v, info):
        smiles = info.data.get("smiles")
        if smiles:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                return float(Descriptors.MolWt(mol))
            raise ValueError("Invalid SMILES string provided.")
        return v
