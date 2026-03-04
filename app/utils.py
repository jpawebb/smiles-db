from rdkit import Chem


def validate_smiles(v: str) -> str:
    """Validate and sanitize all SMILES"""
    if not isinstance(v, str):
        raise TypeError(f"SMILES is not a string, it is {type(v)}")

    mol = Chem.MolFromSmiles(v)
    if mol is None:
        raise ValueError(f"Invalid SMILES string: {v}")
    return Chem.MolToSmiles(mol)
