from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.audit import write_audit_log
import json


# Treatment Plans
def create_plan(db: Session, data: dict):
    q = text("""
        INSERT INTO treatment_plans (client_id, version, status, created_by)
        VALUES (:client_id, :version, :status, :created_by)
        RETURNING id
    """)
    r = db.execute(q, data)
    new_id = r.scalar()
    db.commit()
    return get_plan(db, new_id)


def get_plan(db: Session, plan_id: int):
    q = text("""
        SELECT id, client_id, version, status, needs, media, created_by, created_at
        FROM treatment_plans WHERE id = :id
    """)
    return db.execute(q, {"id": plan_id}).mappings().first()


def get_plan_by_client(db: Session, client_id: int):
    q = text("""
        SELECT id, client_id, version, status, needs, media, created_by, created_at
        FROM treatment_plans
        WHERE client_id = :client_id
        ORDER BY version DESC
        LIMIT 1
    """)
    return db.execute(q, {"client_id": client_id}).mappings().first()


def list_plans_by_client(db: Session, client_id: int):
    q = text("""
        SELECT id, client_id, version, status, needs, media, created_by, created_at
        FROM treatment_plans WHERE client_id = :client_id ORDER BY version DESC
    """)
    return db.execute(q, {"client_id": client_id}).mappings().all()


def update_plan(db: Session, plan_id: int, data: dict):
    q = text("""
        UPDATE treatment_plans
        SET status = COALESCE(:status, status),
            version = COALESCE(:version, version)
        WHERE id = :id
        RETURNING id
    """)
    r = db.execute(q, {"id": plan_id, **data})
    updated_id = r.scalar()
    if not updated_id:
        return None
    db.commit()
    return get_plan(db, updated_id)


def delete_plan(db: Session, plan_id: int):
    q = text("DELETE FROM treatment_plans WHERE id = :id RETURNING id")
    r = db.execute(q, {"id": plan_id})
    db.commit()
    return r.scalar() is not None


def upsert_plan(db: Session, client_id: int, needs: list, media: list, user_id: int = None):
    q = text("""
        INSERT INTO treatment_plans (client_id, version, status, needs, media)
        VALUES (:client_id, 1, 'draft', :needs, :media)
        ON CONFLICT (client_id, version)
        DO UPDATE SET
            needs = EXCLUDED.needs,
            media = EXCLUDED.media
        RETURNING id, client_id, version, status, needs, media, created_by, created_at
    """)
    r = db.execute(q, {
        "client_id": client_id,
        "needs": json.dumps(needs),
        "media": json.dumps(media)
    })
    db.commit()
    row = r.mappings().first()
    write_audit_log(db, user_id, "upsert", "treatment_plan", row["id"],
                    {"needs_count": len(needs), "media_count": len(media)})
    return row


# Goals
def create_goal(db: Session, data: dict):
    q = text("""
        INSERT INTO treatment_goals (treatment_plan_id, title, description, status, sort_order)
        VALUES (:treatment_plan_id, :title, :description, :status, :sort_order)
        RETURNING id
    """)
    r = db.execute(q, data)
    new_id = r.scalar()
    db.commit()
    return get_goal(db, new_id)


def get_goal(db: Session, goal_id: int):
    q = text("""
        SELECT id, treatment_plan_id, title, description, status, sort_order
        FROM treatment_goals WHERE id = :id
    """)
    return db.execute(q, {"id": goal_id}).mappings().first()


def list_goals_by_plan(db: Session, plan_id: int):
    q = text("""
        SELECT id, treatment_plan_id, title, description, status, sort_order
        FROM treatment_goals WHERE treatment_plan_id = :plan_id
        ORDER BY sort_order
    """)
    return db.execute(q, {"plan_id": plan_id}).mappings().all()


def update_goal(db: Session, goal_id: int, data: dict):
    q = text("""
        UPDATE treatment_goals
        SET title = COALESCE(:title, title),
            description = COALESCE(:description, description),
            status = COALESCE(:status, status),
            sort_order = COALESCE(:sort_order, sort_order)
        WHERE id = :id
        RETURNING id
    """)
    r = db.execute(q, {"id": goal_id, **data})
    updated_id = r.scalar()
    if not updated_id:
        return None
    db.commit()
    return get_goal(db, updated_id)


def delete_goal(db: Session, goal_id: int):
    q = text("DELETE FROM treatment_goals WHERE id = :id RETURNING id")
    r = db.execute(q, {"id": goal_id})
    db.commit()
    return r.scalar() is not None


# Objectives
def create_objective(db: Session, data: dict):
    q = text("""
        INSERT INTO goal_objectives (goal_id, description, measure, target, status, sort_order)
        VALUES (:goal_id, :description, :measure, :target, :status, :sort_order)
        RETURNING id
    """)
    r = db.execute(q, data)
    new_id = r.scalar()
    db.commit()
    return get_objective(db, new_id)


def get_objective(db: Session, objective_id: int):
    q = text("""
        SELECT id, goal_id, description, measure, target, status, sort_order
        FROM goal_objectives WHERE id = :id
    """)
    return db.execute(q, {"id": objective_id}).mappings().first()


def list_objectives_by_goal(db: Session, goal_id: int):
    q = text("""
        SELECT id, goal_id, description, measure, target, status, sort_order
        FROM goal_objectives WHERE goal_id = :goal_id
        ORDER BY sort_order
    """)
    return db.execute(q, {"goal_id": goal_id}).mappings().all()


def update_objective(db: Session, objective_id: int, data: dict):
    q = text("""
        UPDATE goal_objectives
        SET description = COALESCE(:description, description),
            measure = COALESCE(:measure, measure),
            target = COALESCE(:target, target),
            status = COALESCE(:status, status),
            sort_order = COALESCE(:sort_order, sort_order)
        WHERE id = :id
        RETURNING id
    """)
    r = db.execute(q, {"id": objective_id, **data})
    updated_id = r.scalar()
    if not updated_id:
        return None
    db.commit()
    return get_objective(db, updated_id)


def delete_objective(db: Session, objective_id: int):
    q = text("DELETE FROM goal_objectives WHERE id = :id RETURNING id")
    r = db.execute(q, {"id": objective_id})
    db.commit()
    return r.scalar() is not None


# Interventions
def create_intervention(db: Session, data: dict):
    q = text("""
        INSERT INTO objective_interventions (objective_id, description, frequency, responsible, sort_order)
        VALUES (:objective_id, :description, :frequency, :responsible, :sort_order)
        RETURNING id
    """)
    r = db.execute(q, data)
    new_id = r.scalar()
    db.commit()
    return get_intervention(db, new_id)


def get_intervention(db: Session, intervention_id: int):
    q = text("""
        SELECT id, objective_id, description, frequency, responsible, sort_order
        FROM objective_interventions WHERE id = :id
    """)
    return db.execute(q, {"id": intervention_id}).mappings().first()


def list_interventions_by_objective(db: Session, objective_id: int):
    q = text("""
        SELECT id, objective_id, description, frequency, responsible, sort_order
        FROM objective_interventions WHERE objective_id = :objective_id
        ORDER BY sort_order
    """)
    return db.execute(q, {"objective_id": objective_id}).mappings().all()


def update_intervention(db: Session, intervention_id: int, data: dict):
    q = text("""
        UPDATE objective_interventions
        SET description = COALESCE(:description, description),
            frequency = COALESCE(:frequency, frequency),
            responsible = COALESCE(:responsible, responsible),
            sort_order = COALESCE(:sort_order, sort_order)
        WHERE id = :id
        RETURNING id
    """)
    r = db.execute(q, {"id": intervention_id, **data})
    updated_id = r.scalar()
    if not updated_id:
        return None
    db.commit()
    return get_intervention(db, updated_id)


def delete_intervention(db: Session, intervention_id: int):
    q = text("DELETE FROM objective_interventions WHERE id = :id RETURNING id")
    r = db.execute(q, {"id": intervention_id})
    db.commit()
    return r.scalar() is not None