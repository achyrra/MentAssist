from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NoteCreate(BaseModel):
    client_id: int
    appointment_id: Optional[int] = None
    note_text: str = Field(..., max_length=10000)
    created_by: Optional[int] = None


class NoteUpdate(BaseModel):
    note_text: str


class NoteOut(BaseModel):
    id: int
    client_id: int
    appointment_id: Optional[int]
    note_text: str
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ClientNoteCreate(BaseModel):
    content: str


class ClientNoteOut(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True