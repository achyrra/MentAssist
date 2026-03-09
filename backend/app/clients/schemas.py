from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ClientCreate(BaseModel):
    counselor_id: int
    first_name: str
    last_name: str
    dob: Optional[date] = None

class ClientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None

class ClientOut(BaseModel):
    id: int
    counselor_id: int
    first_name: str
    last_name: str
    dob: Optional[date]
    created_at: datetime