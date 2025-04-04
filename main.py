from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

import app.routes.users as users
import app.routes.auth as auth
import app.routes.permissions as permissions
import app.routes.roles as roles
import app.routes.user_roles as user_roles
import app.routes.role_permissions as role_permissions

app = FastAPI()

origins = [
    "https://cinesense.dzuverovic.me"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,   
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "running"}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(permissions.router)
app.include_router(roles.router)
app.include_router(user_roles.router)
app.include_router(role_permissions.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
