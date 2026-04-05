from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password, hash_password
from app.core.audit import write_audit_log
from app.db.session import get_db
from . import repo
from .schemas import UserCreate, UserOut, UserLogin

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = repo.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    if payload.role not in ("counselor", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role")
    password_hash = hash_password(payload.password)
    user = repo.create_user(db, payload.email, password_hash, payload.role, payload.first_name, payload.last_name)
    write_audit_log(db, user["id"], "register", "user", user["id"])
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = repo.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user["status"] != "active":
        raise HTTPException(status_code=403, detail="User account is disabled")
    token = create_access_token(user["id"], user["role"])
    write_audit_log(db, user["id"], "login", "user", user["id"])
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