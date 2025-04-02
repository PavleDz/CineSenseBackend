from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Response

import app.database as database
import app.services.auth_service as auth_service
import app.schemas.auth_schema as auth_schema

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#login post, vraca jwt i postalvja ga u http-only cookie
@router.post("/login", response_model=auth_schema.TokenResponse)
def login(data: auth_schema.LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, data.email, data.password)
    token = auth_service.create_access_token({"sub": user.email})

    # cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # promijeni u True ako koristiš HTTPS
        samesite="lax",
        max_age=1800
    )

    return {"access_token": token}
