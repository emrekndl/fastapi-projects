import contextlib
from typing import AsyncIterator

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from logfparse.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# background_task_engine = create_async_engine(
#     settings.DATABASE_URL, echo=False, pool_size=5, max_overflow=10
# )
# BackgroundAsyncSessionLocal = async_sessionmaker(
#     bind=background_task_engine, class_=AsyncSession, expire_on_commit=False
# )


Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self):
        self._sessionmaker = AsyncSessionLocal

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self._sessionmaker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Session error: {e}")
            raise RuntimeError("An error occurred with the session.")
        finally:
            if session.is_active:
                await session.close()


session_manager = DatabaseSessionManager()


async def get_db():
    async with session_manager.session() as session:
        yield session


# async def get_background_db() -> AsyncIterator[AsyncSession]:
#     async with BackgroundAsyncSessionLocal() as session:
#         try:
#             yield session
#         except Exception as e:
#             logger.error(f"Background DB Error: {e}")
#             raise
#         finally:
#             if session.in_transaction():
#                 await session.rollback()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
