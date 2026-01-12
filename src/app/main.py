from fastapi import FastAPI
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager

from src.presentation.api.deps import get_db_config
from src.infrastructure.log.logger import logger
from src.presentation.api.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db_config()
    try:
        await db.connect()
        yield
    except Exception as e:
        logger.exception(f"Asynccontextmanager error: {e}")
        raise
    finally:
        await db.disconnect()

bearer = HTTPBearer()
app = FastAPI(title="FastAPI DDD Template", lifespan=lifespan)
app.include_router(auth.router)