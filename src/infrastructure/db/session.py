from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.db.models import Base
from src.infrastructure.log.logger import logger

from typing import Optional

class DataBaseConfig:
    def __init__(self):
        self._url_database = "sqlite+aiosqlite:///database.db"
        self._async_engine: Optional[AsyncEngine] = None
        self._async_session: Optional[async_sessionmaker[AsyncSession]] = None
    
    @property
    def async_engine(self) -> AsyncEngine:
        if self._async_engine is None:
            try:
                self._async_engine = create_async_engine(
                    self._url_database,
                )
            except SQLAlchemyError as e:
                logger.exception(f"SQLAlchemyError on init async-engine: {e}")
                raise
        return self._async_engine
    
    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        if self._async_session is None:
            try:
                self._async_session = async_sessionmaker(
                    self.async_engine, expire_on_commit=False,
                )
            except SQLAlchemyError as e:
                logger.exception(f"SQLAlchemyError on init async-session: {e}")
                raise
        return self._async_session
    
    async def connect(self) -> None:
        try:
            async with self.async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("database connect successfully")
        except Exception as e:
            logger.exception(f"connect error: {e}")
            raise
    
    async def disconnect(self) -> None:
        try:
            await self.async_engine.dispose()
            logger.info("database disconnect successfully")
        except Exception as e:
            logger.exception(f"disconnect error: {e}")
            raise
