from sqlalchemy import text
from app.db.session import engine


def create_appointment(data: dict):
    q = text("""
        INSERT INTO appointments (client_id, scheduled_at, location, created_by)
        VALUES (:client_id, :scheduled_at, :location, :created_by)
        RETURNING id, client_id, scheduled_at, location, created_by, created_at
    """)
    with engine.begin() as conn:
        r = conn.execute(q, data)
        return r.mappings().first()


def list_appointments():
    q = text("""
        SELECT id, client_id, scheduled_at, location, created_by, created_at
        FROM appointments
        ORDER BY scheduled_at DESC
    """)
    with engine.connect() as conn:
        r = conn.execute(q)
        return r.mappings().all()


def get_appointment(appointment_id: int):
    q = text("""
        SELECT id, client_id, scheduled_at, location, created_by, created_at
        FROM appointments
        WHERE id = :id
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"id": appointment_id})
        return r.mappings().first()


def update_appointment(appointment_id: int, data: dict):
    q = text("""
        UPDATE appointments
        SET scheduled_at = COALESCE(:scheduled_at, scheduled_at),
            location = COALESCE(:location, location)
        WHERE id = :id
        RETURNING id, client_id, scheduled_at, location, created_by, created_at
    """)
    params = {"id": appointment_id, **data}
    with engine.begin() as conn:
        r = conn.execute(q, params)
        return r.mappings().first()


def delete_appointment(appointment_id: int):
    q = text("""
        DELETE FROM appointments
        WHERE id = :id
        RETURNING id
    """)
    with engine.begin() as conn:
        r = conn.execute(q, {"id": appointment_id})
        return r.mappings().first() is not None
