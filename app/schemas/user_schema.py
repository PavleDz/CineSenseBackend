from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.schemas.role_schema import RoleRead
import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class UserRead(UserBase):
    id: int
    created_at: datetime.datetime
    roles: Optional[List[RoleRead]] = []

    class Config:
        from_attributes = True
