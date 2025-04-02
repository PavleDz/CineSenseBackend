from pydantic import BaseModel
from typing import Optional, List
from app.schemas.permission_schema import PermissionRead

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: int
    permissions: Optional[List[PermissionRead]] = []

    class Config:
        from_attributes = True
