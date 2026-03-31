from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from .schemas import ClientCreate, ClientUpdate, ClientOut
from . import repo
from app.notes import repo as notes_repo
from app.notes.schemas import ClientNoteCreate, ClientNoteOut

router = APIRouter()


@router.post("", status_code=201, response_model=ClientOut)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.create_client(db, payload.model_dump())


@router.get("", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "admin":
        return repo.list_clients(db, counselor_id=None)
    return repo.list_clients(db, counselor_id=current_user["id"])


@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    updated = repo.update_client(db, client_id, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated


@router.post("/{client_id}/notes", response_model=ClientNoteOut, status_code=status.HTTP_201_CREATED)
def create_client_note(client_id: int, payload: ClientNoteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    note = notes_repo.create_note(db, {
        "client_id": client_id,
        "note_text": payload.content,
        "appointment_id": None,
        "created_by": current_user["id"]
    })
    return {"id": note["id"], "content": note["note_text"], "created_at": note["created_at"]}


@router.get("/{client_id}/notes", response_model=list[ClientNoteOut])
def list_client_notes(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    notes = notes_repo.list_notes_by_client(db, client_id)
    return [{"id": n["id"], "content": n["note_text"], "created_at": n["created_at"]} for n in notes]