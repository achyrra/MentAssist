from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from . import repo
from .schemas import NoteCreate, NoteUpdate, NoteOut

router = APIRouter()


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.create_note(db, payload.model_dump())


@router.get("/client/{client_id}", response_model=list[NoteOut])
def list_notes(
    client_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repo.list_notes_by_client(db, client_id, limit=limit, offset=offset)


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    note = repo.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.patch("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    note = repo.update_note(db, note_id, payload.model_dump())
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ok = repo.delete_note(db, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")