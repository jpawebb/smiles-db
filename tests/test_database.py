import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_database_connection(db_session):
    """Smoke test to verify connectivity and responsiveness"""
    # SQL ping
    result = await db_session.execute(text("SELECT 1"))
    value = result.scalar_one()
    assert value == 1
