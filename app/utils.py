from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from rdkit import Chem

from app.config import security_settings


def validate_smiles(v: str) -> str:
    """Validate and sanitize all SMILES"""
    if not isinstance(v, str):
        raise TypeError(f"SMILES is not a string, it is {type(v)}")

    mol = Chem.MolFromSmiles(v)
    if mol is None:
        raise ValueError(f"Invalid SMILES string: {v}")
    return Chem.MolToSmiles(mol)


def generate_access_token(data: dict, expiry: timedelta = timedelta(minutes=30)):
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET,
    )
