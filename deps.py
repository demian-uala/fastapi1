from init_db import SessionManager
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from typing import AsyncIterator, Annotated
from fastapi import Depends
from config import get_settings, Settings


Config = Annotated[Settings, Depends(get_settings)]


async def get_sql_session() -> AsyncIterator[AsyncConnection]:
    async with SessionManager.session() as session:
        yield session

SQLSession = Annotated[AsyncSession, Depends(get_sql_session)]
