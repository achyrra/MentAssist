from sqlalchemy.orm import Session
from sqlalchemy import text
import json


def write_audit_log(
    db: Session,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int = None,
    details: dict = None,
):
    q = text("""
        INSERT INTO audit_log (user_id, action, entity_type, entity_id, details)
        VALUES (:user_id, :action, :entity_type, :entity_id, :details)
    """)
    db.execute(q, {
        "user_id":     user_id,
        "action":      action,
        "entity_type": entity_type,
        "entity_id":   entity_id,
        "details":     json.dumps(details) if details else None,
    })
    db.commit()