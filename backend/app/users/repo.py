from sqlalchemy import text
from app.db.session import engine


def create_user(email: str, password_hash: str, role: str = "counselor"):
    q = text("""
        INSERT INTO users (email, password_hash, role)
        VALUES (:email, :password_hash, :role)
        RETURNING id, email, role, status, created_at
    """)
    with engine.begin() as conn:
        r = conn.execute(q, {"email": email, "password_hash": password_hash, "role": role})
        return r.mappings().first()


def get_user_by_email(email: str):
    q = text("""
        SELECT id, email, password_hash, role, status, created_at
        FROM users
        WHERE email = :email
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"email": email})
        return r.mappings().first()


def get_user_by_id(user_id: int):
    q = text("""
        SELECT id, email, role, status, created_at
        FROM users
        WHERE id = :id
    """)
    with engine.connect() as conn:
        r = conn.execute(q, {"id": user_id})
        return r.mappings().first()


def list_users():
    q = text("""
        SELECT id, email, role, status, created_at
        FROM users
        ORDER BY id
    """)
    with engine.connect() as conn:
        r = conn.execute(q)
        return r.mappings().all()
