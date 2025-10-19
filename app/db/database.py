from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from app.core.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    """
    Ensure schema exists and create tables in that schema.
    """
    async with engine.begin() as conn:
        # Create schema if not exists
        await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{settings.db_schema}"'))
        # Set search_path for create_all
        await conn.execute(text(f'SET search_path TO "{settings.db_schema}"'))
        await conn.run_sync(Base.metadata.create_all)
