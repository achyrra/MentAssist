from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "counselor"
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    status: str
    created_at: datetime
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
