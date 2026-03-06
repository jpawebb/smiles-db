from pydantic import BaseModel, field_validator
from rdkit import Chem


class SmilesCreate(BaseModel):
    smiles: str

    @field_validator("smiles")
    @classmethod
    def validate_smile(cls, v: str):
        mol = Chem.MolFromSmiles(v)
        if mol is None:
            raise ValueError("This is not a valid SMILES string")
        return Chem.MolToSmiles(mol, isomericSmiles=True)
