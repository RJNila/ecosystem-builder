from fastapi import FastAPI
from app.api.v1.routes.organization import router as org_router
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(
    title="Ecosystem Builder",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include versioned routes
app.include_router(org_router, prefix="/api/v1", tags=["organizations"])

@app.on_event("startup")
async def on_startup():
    # Create schema + tables if not present (dev-friendly)
    await init_db()

@app.get("/healthz")
async def health():
    return {"status": "ok", "env": settings.app_env}
