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
    """Creates the JWT access token

    Raises:
        jwt.PyJWTError: If there is any error generating the token
    """
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET,
    )


def decode_access_token(token: str) -> dict:
    """Decodes the JWT access token

    Raises:
        jwt.ExpiredSignatureError: If the token has expired
        jwt.InvalidTokenError: If the token is invalid for any reason
    """
    return jwt.decode(
        token,
        key=security_settings.JWT_SECRET,
        algorithms=[security_settings.JWT_ALGORITHM],
    )
