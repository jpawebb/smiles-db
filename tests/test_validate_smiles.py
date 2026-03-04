import pytest
from app.utils import validate_smiles


@pytest.mark.parametrize(
    "v,expected",
    [
        # Valid benzene
        ("c1ccccc1", "c1ccccc1"),
        # Non-standard Kekule benzene
        ("C1=CC=CC=C1", "c1ccccc1"),
        # Invalid broken smile :(
        ("CC(CCCC", ValueError),
        # Type enforcement
        (10.0, TypeError),
    ],
)
def test_validate_smiles(v, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            validate_smiles(v)
    else:
        actual = validate_smiles(v)
        assert actual == expected
