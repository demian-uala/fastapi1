from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncIterator
import contextlib
from config import get_settings


settings = {
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    # 'echo': True,
    'future': True,
}


class DatabaseException(Exception):
    pass


def get_conn_url():
    s = get_settings()
    return f"postgresql+asyncpg://{s.DB_USER}:{s.DB_PASS}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"


class SQLSessionManager:
    def __init__(self, host: str = get_conn_url(), engine_kwargs: dict = settings):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

    async def close(self):
        if self._engine is None:
            raise DatabaseException(f"{self.__class__.__name__} is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DatabaseException(f"{self.__class__.__name__} is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DatabaseException(f"{self.__class__.__name__} is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


SessionManager = SQLSessionManager()
