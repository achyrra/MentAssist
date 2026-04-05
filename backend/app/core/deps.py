from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.users import repo
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = repo.get_user_by_id(db, int(payload["sub"]))
    if not user or user["status"] != "active":
        raise HTTPException(status_code=401, detail="User not found or disabled")
    return user

def assert_client_access(client, current_user: dict):
    """Helper to check if the current user has access to the given client."""
    if current_user["role"] == "admin":
        return
    if client["counselor_id"] != current_user["id"]:
        """using 404 to avoid revealing existence of client to unauthorized users"""
        raise HTTPException(status_code=404, detail="Client not found")