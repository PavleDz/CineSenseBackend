import jwt
import datetime
from passlib.hash import bcrypt
from fastapi import HTTPException,Request, Depends
import sqlalchemy as sql
from sqlalchemy import select
from dotenv import dotenv_values

import app.database as database
import app.models as models
from app.schemas.user_schema import UserCreate

env = dotenv_values(".env")

SECRET_KEY = env.get("SECRET_KEY")
ALGORITHM = env.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(env.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

def authenticate_user(db: sql.orm.Session, email: str, password: str):
    stmt = select(models.User).where(models.User.email == email)
    user = db.execute(stmt).scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(request: Request, db: sql.orm.Session = Depends(database.SessionLocal)):
    token = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    stmt = select(models.User).where(models.User.email == email)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def register_user(db: sql.orm.Session, user_data: UserCreate) -> models.User:
    existing = db.execute(select(models.User).where(models.User.email == user_data.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = bcrypt.hash(user_data.password)

    try:
        default_role = db.execute(select(models.Role).where(models.Role.name == 'user')).scalar_one()
        user = models.User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            roles=[default_role]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
