from sqlalchemy.orm import Session
from sqlalchemy import text


def create_appointment(db: Session, data: dict):
    q = text("""
        INSERT INTO appointments (client_id, scheduled_at, location, created_by)
        VALUES (:client_id, :scheduled_at, :location, :created_by)
        RETURNING id, client_id, scheduled_at, location, created_by, created_at
    """)
    r = db.execute(q, data)
    db.commit()
    return r.mappings().first()


def list_appointments(db: Session):
    q = text("""
        SELECT id, client_id, scheduled_at, location, created_by, created_at
        FROM appointments
        ORDER BY scheduled_at DESC
    """)
    r = db.execute(q)
    return r.mappings().all()


def get_appointment(db: Session, appointment_id: int):
    q = text("""
        SELECT id, client_id, scheduled_at, location, created_by, created_at
        FROM appointments
        WHERE id = :id
    """)
    r = db.execute(q, {"id": appointment_id})
    return r.mappings().first()


def update_appointment(db: Session, appointment_id: int, data: dict):
    q = text("""
        UPDATE appointments
        SET scheduled_at = COALESCE(:scheduled_at, scheduled_at),
            location = COALESCE(:location, location)
        WHERE id = :id
        RETURNING id, client_id, scheduled_at, location, created_by, created_at
    """)
    r = db.execute(q, {"id": appointment_id, **data})
    db.commit()
    return r.mappings().first()


def delete_appointment(db: Session, appointment_id: int):
    q = text("""
        DELETE FROM appointments
        WHERE id = :id
        RETURNING id
    """)
    r = db.execute(q, {"id": appointment_id})
    db.commit()
    return r.mappings().first() is not None