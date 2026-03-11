from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base


class TreatmentPlan(Base):
    __tablename__ = "treatment_plans"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    version = Column(Integer, nullable=False)
    status = Column(Text, nullable=False, default="draft")
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class TreatmentGoal(Base):
    __tablename__ = "treatment_goals"

    id = Column(Integer, primary_key=True)
    treatment_plan_id = Column(Integer, ForeignKey("treatment_plans.id"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    status = Column(Text, nullable=False, default="active")
    sort_order = Column(Integer, default=0)


class GoalObjective(Base):
    __tablename__ = "goal_objectives"

    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer, ForeignKey("treatment_goals.id"), nullable=False)
    description = Column(Text, nullable=False)
    measure = Column(Text)
    target = Column(Text)
    status = Column(Text, nullable=False, default="active")
    sort_order = Column(Integer, default=0)


class ObjectiveIntervention(Base):
    __tablename__ = "objective_interventions"

    id = Column(Integer, primary_key=True)
    objective_id = Column(Integer, ForeignKey("goal_objectives.id"), nullable=False)
    description = Column(Text, nullable=False)
    frequency = Column(Text)
    responsible = Column(Text)
    sort_order = Column(Integer, default=0)