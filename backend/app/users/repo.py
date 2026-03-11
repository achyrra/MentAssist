from sqlalchemy.orm import Session
from sqlalchemy import text


def create_user(db: Session, email: str, password_hash: str, role: str = "counselor", first_name: str = None, last_name: str = None):
    q = text("""
        INSERT INTO users (email, password_hash, role, first_name, last_name)
        VALUES (:email, :password_hash, :role, :first_name, :last_name)
        RETURNING id
    """)
    r = db.execute(q, {"email": email, "password_hash": password_hash, "role": role, "first_name": first_name, "last_name": last_name})
    new_id = r.scalar()
    db.commit()
    return get_user_by_id(db, new_id)


def get_user_by_email(db: Session, email: str):
    q = text("""
        SELECT id, email, password_hash, role, status, created_at, first_name, last_name
        FROM users
        WHERE email = :email
    """)
    r = db.execute(q, {"email": email})
    return r.mappings().first()


def get_user_by_id(db: Session, user_id: int):
    q = text("""
        SELECT id, email, role, status, created_at, first_name, last_name
        FROM users
        WHERE id = :id
    """)
    r = db.execute(q, {"id": user_id})
    return r.mappings().first()


def list_users(db: Session):
    q = text("""
        SELECT id, email, role, status, created_at, first_name, last_name
        FROM users
        ORDER BY id
    """)
    r = db.execute(q)
    return r.mappings().all()