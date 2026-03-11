from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    client_id: int = Field(..., ge=1)
    scheduled_at: datetime
    location: Optional[str] = None
    created_by: Optional[int] = None


class AppointmentUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    location: Optional[str] = None


class AppointmentOut(BaseModel):
    id: int
    client_id: int
    scheduled_at: datetime
    location: Optional[str]
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True