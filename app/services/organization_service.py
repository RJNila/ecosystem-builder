from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dtos.organization import OrganizationCreate
from app.db.models.organization import Organization

class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_code(self, code: str) -> Organization | None:
        res = await self.db.execute(select(Organization).where(Organization.code == code))
        return res.scalar_one_or_none()

    async def create(self, dto: OrganizationCreate) -> Organization:
        org = Organization(name=dto.name, code=dto.code, description=dto.description)
        self.db.add(org)
        await self.db.commit()
        await self.db.refresh(org)
        return org
