from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.database as database
import app.services.user_service as user_service
import app.schemas.user_schema as user_schema


router = APIRouter(prefix="/api/users", tags=["Users"])

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get all
@router.get("/", response_model=List[user_schema.UserRead])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

# get by id
@router.get("/{user_id}", response_model=user_schema.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# get by username
@router.get("/{username}", response_model=user_schema.UserRead)
def get_user(username: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# get by email
@router.get("/{email}", response_model=user_schema.UserRead)
def get_user(email: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# add
@router.post("/", response_model=user_schema.UserRead, status_code=201)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing = user_service.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db, user)

# update
@router.put("/{user_id}", response_model=user_schema.UserRead)
def update_user(user_id: int, user_data: user_schema.UserUpdate, db: Session = Depends(get_db)):
    updated = user_service.update_user(db, user_id, user_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

# delete by id
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not user_service.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return
