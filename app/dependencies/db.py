from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for s in get_session():
        yield s
