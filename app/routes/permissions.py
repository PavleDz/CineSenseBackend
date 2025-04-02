from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.database as database
import app.services.permission_service as permission_service
import app.schemas.permission_schema as permission_schema

router = APIRouter(prefix="/api/permissions", tags=["Permissions"])

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get all
@router.get("/", response_model=List[permission_schema.PermissionRead])
def get_permissions(db: Session = Depends(get_db)):
    return permission_service.get_all_permissions(db)

# get by id
@router.get("/{permission_id}", response_model=permission_schema.PermissionRead)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    perm = permission_service.get_permission_by_id(db, permission_id)
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    return perm

# add
@router.post("/", response_model=permission_schema.PermissionRead, status_code=201)
def create_permission(data: permission_schema.PermissionCreate, db: Session = Depends(get_db)):
    return permission_service.create_permission(db, data)

# update
@router.put("/{permission_id}", response_model=permission_schema.PermissionRead)
def update_permission(permission_id: int, data: permission_schema.PermissionUpdate, db: Session = Depends(get_db)):
    updated = permission_service.update_permission(db, permission_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Permission not found")
    return updated

# delete by id
@router.delete("/{permission_id}", status_code=204)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    if not permission_service.delete_permission(db, permission_id):
        raise HTTPException(status_code=404, detail="Permission not found")
    return
