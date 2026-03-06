from fastapi import APIRouter, HTTPException, status

from .repo import AppointmentRepo
from .schemas import AppointmentCreate, AppointmentOut, AppointmentUpdate

router = APIRouter(prefix="/appointments", tags=["appointments"])
_repo = AppointmentRepo()


@router.get("/", response_model=list[AppointmentOut])
def list_appointments():
    return _repo.list()


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int):
    appt = _repo.get(appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate):
    return _repo.create(payload)


@router.patch("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, payload: AppointmentUpdate):
    appt = _repo.update(appointment_id, payload)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int):
    ok = _repo.delete(appointment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return None