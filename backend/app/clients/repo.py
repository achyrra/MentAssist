from sqlalchemy.orm import Session
from sqlalchemy import text


def create_client(db: Session, data: dict):
    q = text("""
        INSERT INTO clients (counselor_id, first_name, last_name, dob)
        VALUES (:counselor_id, :first_name, :last_name, :dob)
        RETURNING id, counselor_id, first_name, last_name, dob, created_at
    """)
    r = db.execute(q, data)
    db.commit()
    return r.mappings().first()


def list_clients(db: Session, counselor_id: int = None):
    if counselor_id is None:
        q = text("""
            SELECT id, counselor_id, first_name, last_name, dob, created_at
            FROM clients
            ORDER BY id
        """)
        r = db.execute(q)
    else:
        q = text("""
            SELECT id, counselor_id, first_name, last_name, dob, created_at
            FROM clients
            WHERE counselor_id = :counselor_id
            ORDER BY id
        """)
        r = db.execute(q, {"counselor_id": counselor_id})
    return r.mappings().all()


def get_client(db: Session, client_id: int):
    q = text("""
        SELECT id, counselor_id, first_name, last_name, dob, created_at
        FROM clients
        WHERE id = :id
    """)
    r = db.execute(q, {"id": client_id})
    return r.mappings().first()


def update_client(db: Session, client_id: int, data: dict):
    q = text("""
        UPDATE clients
        SET first_name = COALESCE(:first_name, first_name),
            last_name = COALESCE(:last_name, last_name),
            dob = COALESCE(:dob, dob)
        WHERE id = :id
        RETURNING id, counselor_id, first_name, last_name, dob, created_at
    """)
    r = db.execute(q, {"id": client_id, **data})
    db.commit()
    return r.mappings().first()
