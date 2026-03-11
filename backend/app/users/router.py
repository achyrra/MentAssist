from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.core.security import create_access_token, verify_password, hash_password
from . import repo
from .schemas import UserCreate, UserOut
from .schemas import UserLogin

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate):
    existing = repo.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    if payload.role not in ("counselor", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role")

    password_hash = hash_password(payload.password)
    user = repo.create_user(payload.email, password_hash, payload.role, payload.first_name, payload.last_name)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Login endpoint 
@router.post("/login")
def login(payload: UserLogin):
    user = repo.get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user["status"] != "active":
        raise HTTPException(status_code=403, detail="User account is disabled")
    
    token = create_access_token(user["id"], user["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "first_name": user["first_name"],
            "last_name": user["last_name"]
        }
    }