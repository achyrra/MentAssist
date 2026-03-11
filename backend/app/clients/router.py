from fastapi import APIRouter, HTTPException
from .schemas import ClientCreate, ClientUpdate
from . import repo

router = APIRouter()

@router.post("", status_code=201)
def create_client(payload: ClientCreate):
    created = repo.create_client(payload.model_dump())
    return created

@router.get("")
def list_clients():
    return repo.list_clients()

@router.get("/{client_id}")
def get_client(client_id: int):
    client = repo.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}")
def update_client(client_id: int, payload: ClientUpdate):
    updated = repo.update_client(client_id, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated