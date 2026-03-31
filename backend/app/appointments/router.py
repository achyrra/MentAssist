from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from . import repo
from .schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut

router = APIRouter()


@router.get("", response_model=list[AppointmentOut])
def list_appointments(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.list_appointments(db)


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    appt = repo.get_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    data = payload.model_dump()
    data.setdefault("created_by", None)
    return repo.create_appointment(db, data)


@router.patch("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, payload: AppointmentUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    appt = repo.update_appointment(db, appointment_id, payload.model_dump())
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ok = repo.delete_appointment(db, appointment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Appointment not found")