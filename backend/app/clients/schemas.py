from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional


class ClientCreate(BaseModel):
    counselor_id: int
    first_name: str
    last_name: str
    dob: Optional[date] = None
    primary_diagnosis: Optional[str] = None
    primary_concerns: Optional[str] = None
    therapy_focus: Optional[str] = None

    @field_validator("dob")
    @classmethod
    def dob_must_be_past(cls, v):
        if v and v >= date.today():
            raise ValueError("dob must be in the past")
        return v


class ClientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    primary_diagnosis: Optional[str] = None
    primary_concerns: Optional[str] = None
    therapy_focus: Optional[str] = None

    @field_validator("dob")
    @classmethod
    def dob_must_be_past(cls, v):
        if v and v >= date.today():
            raise ValueError("dob must be in the past")
        return v


class ClientOut(BaseModel):
    id: int
    counselor_id: int
    first_name: str
    last_name: str
    dob: Optional[date]
    primary_diagnosis: Optional[str]
    primary_concerns: Optional[str]
    therapy_focus: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True