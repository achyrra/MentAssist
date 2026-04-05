from sqlalchemy.orm import Session
from sqlalchemy import text
import json


def list_resources(db: Session, limit: int = 50, offset: int = 0):
    q = text("""
        SELECT id, title, type, tags, file_name, mime_type, created_by, created_at
        FROM resources ORDER BY created_at DESC LIMIT :limit OFFSET :offset
    """)
    return db.execute(q, {"limit": limit, "offset": offset}).mappings().all()


def get_resource(db: Session, resource_id: int):
    q = text("""
        SELECT id, title, type, tags, file_name, mime_type, file_data, created_by, created_at
        FROM resources WHERE id = :id
    """)
    return db.execute(q, {"id": resource_id}).mappings().first()


def create_resource(db: Session, data: dict):
    q = text("""
        INSERT INTO resources (title, type, tags, file_name, mime_type, file_data, created_by)
        VALUES (:title, :type, :tags, :file_name, :mime_type, :file_data, :created_by)
        RETURNING id, title, type, tags, file_name, mime_type, created_by, created_at
    """)
    r = db.execute(q, {
        "title":      data["title"],
        "type":       data["type"],
        "tags":       json.dumps(data.get("tags", [])),
        "file_name":  data.get("file_name"),
        "mime_type":  data.get("mime_type"),
        "file_data":  data.get("file_data"),
        "created_by": data.get("created_by"),
    })
    db.commit()
    return r.mappings().first()


def delete_resource(db: Session, resource_id: int) -> bool:
    q = text("DELETE FROM resources WHERE id = :id RETURNING id")
    r = db.execute(q, {"id": resource_id})
    db.commit()
    return r.scalar() is not None