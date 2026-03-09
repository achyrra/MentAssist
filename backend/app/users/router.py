import bcrypt
from fastapi import APIRouter, HTTPException
from . import repo
from .schemas import UserCreate, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate):
    existing = repo.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    if payload.role not in ("counselor", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role")

    password_hash = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()
    user = repo.create_user(payload.email, password_hash, payload.role)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Login endpoint intentionally omitted — requires JWT spec from opsec
