from sqlalchemy.orm import Session
from sqlalchemy import text


def create_note(db: Session, data: dict):
    q = text("""
        INSERT INTO session_notes (client_id, appointment_id, note_text, created_by)
        VALUES (:client_id, :appointment_id, :note_text, :created_by)
        RETURNING id
    """)
    r = db.execute(q, data)
    new_id = r.scalar()
    db.commit()
    return get_note(db, new_id)


def get_note(db: Session, note_id: int):
    q = text("""
        SELECT id, client_id, appointment_id, note_text, created_by, created_at
        FROM session_notes
        WHERE id = :id
    """)
    r = db.execute(q, {"id": note_id})
    return r.mappings().first()


def list_notes_by_client(db: Session, client_id: int, limit: int = 50, offset: int = 0):
    q = text("""
        SELECT id, client_id, appointment_id, note_text, created_by, created_at
        FROM session_notes
        WHERE client_id = :client_id
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :offset
    """)
    r = db.execute(q, {"client_id": client_id, "limit": limit, "offset": offset})
    return r.mappings().all()


def update_note(db: Session, note_id: int, data: dict):
    q = text("""
        UPDATE session_notes
        SET note_text = :note_text
        WHERE id = :id
        RETURNING id
    """)
    r = db.execute(q, {"id": note_id, **data})
    updated_id = r.scalar()
    if not updated_id:
        return None
    db.commit()
    return get_note(db, updated_id)


def delete_note(db: Session, note_id: int):
    q = text("""
        DELETE FROM session_notes
        WHERE id = :id
        RETURNING id
    """)
    r = db.execute(q, {"id": note_id})
    db.commit()
    return r.scalar() is not None