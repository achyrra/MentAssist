from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from .schemas import ClientCreate, ClientUpdate, ClientOut
from . import repo

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