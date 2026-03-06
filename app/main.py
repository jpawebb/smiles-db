from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from scalar_fastapi import get_scalar_api_reference
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.api.router import master_router
from app.database.session import get_session, create_db_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(master_router)


@app.get("/health/db")
async def db_health_check(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"db": result.scalar()}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
