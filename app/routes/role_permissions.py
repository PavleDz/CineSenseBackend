from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.database as database
import app.models as models
import app.services.role_service as role_service
import app.services.role_permission_service as rp_service
import app.schemas.role_schema as role_schema

router = APIRouter(prefix="/api/roles", tags=["Role-Permissions"])

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dodavanje role useru
@router.post("/{role_id}/permissions/{permission_id}", response_model=role_schema.RoleRead)
def add_permission(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = role_service.get_role_by_id(db, role_id)
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()

    if not role or not permission:
        raise HTTPException(status_code=404, detail="Role or Permission not found")

    return rp_service.add_permission_to_role(db, role, permission)

# uklanjanje role useru
@router.delete("/{role_id}/permissions/{permission_id}", status_code=204)
def remove_permission(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = role_service.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    rp_service.remove_permission_from_role(db, role, permission_id)
    return
