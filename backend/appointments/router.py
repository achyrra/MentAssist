from fastapi import APIRouter, HTTPException, status
from . import repo
from .schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut

router = APIRouter()


@router.get("/", response_model=list[AppointmentOut])
def list_appointments():
    return repo.list_appointments()


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int):
    appt = repo.get_appointment(appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate):
    data = payload.model_dump()
    data.setdefault("created_by", None)
    return repo.create_appointment(data)


@router.patch("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, payload: AppointmentUpdate):
    appt = repo.update_appointment(appointment_id, payload.model_dump())
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int):
    ok = repo.delete_appointment(appointment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Appointment not found")