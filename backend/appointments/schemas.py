from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AppointmentBase(BaseModel):
    client_id: int = Field(..., ge=1)
    scheduled_at: datetime
    location: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    location: Optional[str] = None


class AppointmentOut(AppointmentBase):
    id: int

    class Config:
        from_attributes = True