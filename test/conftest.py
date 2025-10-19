import asyncio
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

# Ensure repo root is on sys.path so `app` package imports resolve when running pytest
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Do NOT import `app` or `app.db.database` at module import time. Tests need to set
# `config.settings.database_url` before those modules create engines. Import `config`
# only to access settings and then import the app/database inside fixtures after override.
from app.core import config  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def sqlite_url(tmp_path_factory):
    # Use a temporary file-backed SQLite DB for async support
    db_file = tmp_path_factory.mktemp("data") / "test.db"
    return f"sqlite+aiosqlite:///{db_file}"


@pytest.fixture(scope="session")
async def initialized_db(sqlite_url):
    # Override settings for tests
    config.settings.database_url = sqlite_url
    # SQLite does not support schemas; ensure no schema is applied in tests
    config.settings.db_schema = None

    # Import database and models after overriding settings so the module-level
    # engine inside `app.db.database` will be created using the test URL if needed.
    # We'll also create tables using a local engine to avoid relying on module state.
    # Import models so they register their tables onto Base.metadata
    import importlib
    importlib.import_module("app.db.models.organization")
    from app.db.database import Base

    engine = create_async_engine(sqlite_url, future=True)
    async with engine.begin() as conn:
        # SQLite doesn't support schemas; simply create tables
        await conn.run_sync(Base.metadata.create_all)

    yield
    await engine.dispose()


@pytest.fixture
def client(initialized_db):
    # Import the FastAPI app after the DB settings have been overridden and tables created
    from app.main import app

    # If tests use sqlite, skip startup handlers that execute Postgres-specific SQL
    # (init_db creates schemas / sets search_path) which will fail on sqlite.
    try:
        if str(config.settings.database_url).startswith("sqlite"):
            # Clear startup handlers so TestClient doesn't run them
            if hasattr(app, "router") and hasattr(app.router, "on_startup"):
                app.router.on_startup.clear()
    except Exception:
        # Don't fail tests for non-critical clearing; continue to use the app
        pass

    # Provide a TestClient for FastAPI app (sync) - startup events (on_startup) will run
    with TestClient(app) as c:
        yield c
