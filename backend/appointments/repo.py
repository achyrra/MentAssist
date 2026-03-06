from typing import Dict, List, Optional

from .schemas import AppointmentCreate, AppointmentOut, AppointmentUpdate


class AppointmentRepo:
    def __init__(self) -> None:
        self._data: Dict[int, AppointmentOut] = {}
        self._next_id = 1

    def list(self) -> List[AppointmentOut]:
        return list(self._data.values())

    def get(self, appointment_id: int) -> Optional[AppointmentOut]:
        return self._data.get(appointment_id)

    def create(self, payload: AppointmentCreate) -> AppointmentOut:
        appt = AppointmentOut(
            id=self._next_id,
            client_id=payload.client_id,
            scheduled_at=payload.scheduled_at,
            location=payload.location,
        )
        self._data[self._next_id] = appt
        self._next_id += 1
        return appt

    def update(self, appointment_id: int, payload: AppointmentUpdate) -> Optional[AppointmentOut]:
        existing = self._data.get(appointment_id)
        if not existing:
            return None

        updated = existing.model_copy(
            update={
                "scheduled_at": payload.scheduled_at or existing.scheduled_at,
                "location": payload.location if payload.location is not None else existing.location,
            }
        )
        self._data[appointment_id] = updated
        return updated

    def delete(self, appointment_id: int) -> bool:
        return self._data.pop(appointment_id, None) is not None