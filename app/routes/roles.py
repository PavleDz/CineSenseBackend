from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.database as database
import app.services.role_service as role_service
import app.schemas.role_schema as role_schema

router = APIRouter(prefix="/api/roles", tags=["Roles"])

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get all
@router.get("/", response_model=List[role_schema.RoleRead])
def get_roles(db: Session = Depends(get_db)):
    return role_service.get_all_roles(db)

# get by id
@router.get("/{role_id}", response_model=role_schema.RoleRead)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = role_service.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# add 
@router.post("/", response_model=role_schema.RoleRead, status_code=201)
def create_role(role_data: role_schema.RoleCreate, db: Session = Depends(get_db)):
    return role_service.create_role(db, role_data)

# update
@router.put("/{role_id}", response_model=role_schema.RoleRead)
def update_role(role_id: int, role_data: role_schema.RoleUpdate, db: Session = Depends(get_db)):
    updated = role_service.update_role(db, role_id, role_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated


# delete by id
@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    if not role_service.delete_role(db, role_id):
        raise HTTPException(status_code=404, detail="Role not found")
    return
