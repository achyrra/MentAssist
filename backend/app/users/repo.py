from sqlalchemy import text
from app.db.session import engine


def create_user(email: str, password_hash: str, role: str = "counselor", first_name: str = None, last_name: str = None):
    q = text("""
        INSERT INTO users (email, password_hash, role, first_name, last_name)
        VALUES (:email, :password_hash, :role, :first_name, :last_name)
        RETURNING id, email, role, status, created_at, first_name, last_name
    """)
    with engine.begin() as conn:
        r = conn.execute(q, {"email": email, "password_hash": password_hash, "role": role, "first_name": first_name, "last_name": last_name})
        return r.mappings().first()


def get_user_by_email(email: str):
    q = text("""
        SELECT id, email, password_hash, role, status, created_at, first_name, last_name
        FROM users
        WHERE email = :email
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"email": email})
        return r.mappings().first()


def get_user_by_id(user_id: int):
    q = text("""
        SELECT id, email, role, status, created_at, first_name, last_name
        FROM users
        WHERE id = :id
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"id": user_id})
        return r.mappings().first()


def list_users():
    q = text("""
        SELECT id, email, role, status, created_at, first_name, last_name
        FROM users
        ORDER BY id
    """)
    with engine.connect() as conn:
        r = conn.execute(q)
        return r.mappings().all()
