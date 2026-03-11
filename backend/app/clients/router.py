from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from .schemas import ClientCreate, ClientUpdate, ClientOut
from . import repo

router = APIRouter()


@router.post("", status_code=201, response_model=ClientOut)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    return repo.create_client(db, payload.model_dump())


@router.get("", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return repo.list_clients(db)


@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    updated = repo.update_client(db, client_id, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated