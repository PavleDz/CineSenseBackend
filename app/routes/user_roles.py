from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.database as database
import app.models as models
import app.services.user_service as user_service
import app.services.user_role_service as ur_service
import app.schemas.user_schema as user_schema

router = APIRouter(prefix="/api/users", tags=["User-Roles"])

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dodavanje role useru
@router.post("/{user_id}/roles/{role_id}", response_model=user_schema.UserRead)
def add_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    role = db.query(models.Role).filter(models.Role.id == role_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return ur_service.add_role_to_user(db, user, role)

# uklanjanje role useru
@router.delete("/{user_id}/roles/{role_id}", status_code=204)
def remove_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ur_service.remove_role_from_user(db, user, role_id)
    return
