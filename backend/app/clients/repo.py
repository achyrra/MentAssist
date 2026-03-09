from sqlalchemy import text
from app.db.session import engine

def create_client(data: dict):
    q = text("""
        INSERT INTO clients (counselor_id, first_name, last_name, dob)
        VALUES (:counselor_id, :first_name, :last_name, :dob)
        RETURNING id, counselor_id, first_name, last_name, dob, created_at
    """)
    with engine.begin() as conn:
        r = conn.execute(q, data)
        return r.mappings().first()

def list_clients():
    q = text("""
        SELECT id, counselor_id, first_name, last_name, dob, created_at
        FROM clients
        ORDER BY id
    """)
    with engine.connect() as conn:
        r = conn.execute(q)
        return r.mappings().all()

def get_client(client_id: int):
    q = text("""
        SELECT id, counselor_id, first_name, last_name, dob, created_at
        FROM clients
        WHERE id = :id
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"id": client_id})
        return r.mappings().first()

def update_client(client_id: int, data: dict):
    q = text("""
        UPDATE clients
        SET first_name = COALESCE(:first_name, first_name),
            last_name = COALESCE(:last_name, last_name),
            dob = COALESCE(:dob, dob)
        WHERE id = :id
        RETURNING id, counselor_id, first_name, last_name, dob, created_at
    """)
    params = {"id": client_id, **data}
    with engine.begin() as conn:
        r = conn.execute(q, params)
        return r.mappings().first()