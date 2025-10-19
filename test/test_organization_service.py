
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core import config


@pytest.mark.asyncio
async def test_create_and_get_by_code(tmp_path):
    # Prepare sqlite url and override settings BEFORE importing modules that create engines
    url = f"sqlite+aiosqlite:///{tmp_path / 'svc.db'}"
    config.settings.database_url = url
    config.settings.db_schema = "main"

    # Now import database models and service so they pick up overridden settings
    from app.db.database import Base
    from app.services.organization_service import OrganizationService
    from app.dtos.organization import OrganizationCreate

    engine = create_async_engine(url, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        service = OrganizationService(session)
        dto = OrganizationCreate(name="Test Org", code="TST", description="d")
        org = await service.create(dto)
        assert org.id is not None
        f = await service.get_by_code("TST")
        assert f is not None
        assert f.code == "TST"

    await engine.dispose()
