import sqlalchemy as sql
from sqlalchemy import select
from passlib.hash import bcrypt
from typing import List, Optional

import app.models as models
import app.schemas.user_schema as user_schema



def get_user_by_id(db: sql.orm.Session, user_id: int) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_username(db: sql.orm.Session, username: str) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.username == username)
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_email(db: sql.orm.Session, email: str) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.email == email)
    return db.execute(stmt).scalar_one_or_none()

def get_all_users(db: sql.orm.Session) -> List[models.User]:
    stmt = select(models.User)
    return db.execute(stmt).scalars().all()

def create_user(db: sql.orm.Session, user_data: user_schema.UserCreate) -> models.User:
    hashed_password = bcrypt.hash(user_data.password)
    user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: sql.orm.Session, user_id: int, user_data: user_schema.UserUpdate) -> Optional[models.User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    if user_data.username:
        user.username = user_data.username
    if user_data.email:
        user.email = user_data.email
    if user_data.password:
        user.hashed_password = bcrypt.hash(user_data.password)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: sql.orm.Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True