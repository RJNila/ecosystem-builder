from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dtos.organization import OrganizationCreate, OrganizationOut
from app.services.organization_service import OrganizationService

router = APIRouter()

@router.post("/organizations", response_model=OrganizationOut, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    existing = await service.get_by_code(payload.code)
    if existing:
        raise HTTPException(status_code=409, detail="Organization with this code already exists")
    org = await service.create(payload)
    return OrganizationOut.model_validate(org)
