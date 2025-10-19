from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID

class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    code: str = Field(min_length=2, max_length=64)
    description: Optional[str] = Field(default=None, max_length=500)

class OrganizationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    code: str
    description: Optional[str] = None
