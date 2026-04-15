from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.audit import write_audit_log


def create_appointment(db: Session, data: dict):
    q = text("""
        INSERT INTO appointments (client_id, scheduled_at, location, created_by)
        VALUES (:client_id, :scheduled_at, :location, :created_by)
        RETURNING id, client_id, scheduled_at, location, created_by, created_at
    """)
    r = db.execute(q, data)
    db.commit()
    row = r.mappings().first()
    write_audit_log(db, data.get("created_by"), "create", "appointment", row["id"])
    return row


def list_appointments(db: Session, limit: int = 50, offset: int = 0):
    q = text("""
        SELECT id, client_id, scheduled_at, location, created_by, created_at
        FROM appointments
        ORDER BY scheduled_at DESC
        LIMIT :limit OFFSET :offset
    """)
    r = db.execute(q, {"limit": limit, "offset": offset})
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


def delete_appointment(db: Session, appointment_id: int, user_id: int = None):
    q = text("""
        DELETE FROM appointments
        WHERE id = :id
        RETURNING id
    """)
    r = db.execute(q, {"id": appointment_id})
    db.commit()
    deleted = r.scalar() is not None
    if deleted:
        write_audit_log(db, user_id, "delete", "appointment", appointment_id)
    return deleted