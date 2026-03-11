from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InterventionCreate(BaseModel):
    objective_id: int
    description: str
    frequency: Optional[str] = None
    responsible: Optional[str] = None
    sort_order: int = 0


class InterventionUpdate(BaseModel):
    description: Optional[str] = None
    frequency: Optional[str] = None
    responsible: Optional[str] = None
    sort_order: Optional[int] = None


class InterventionOut(BaseModel):
    id: int
    objective_id: int
    description: str
    frequency: Optional[str]
    responsible: Optional[str]
    sort_order: int

    class Config:
        from_attributes = True


class ObjectiveCreate(BaseModel):
    goal_id: int
    description: str
    measure: Optional[str] = None
    target: Optional[str] = None
    status: str = "active"
    sort_order: int = 0


class ObjectiveUpdate(BaseModel):
    description: Optional[str] = None
    measure: Optional[str] = None
    target: Optional[str] = None
    status: Optional[str] = None
    sort_order: Optional[int] = None


class ObjectiveOut(BaseModel):
    id: int
    goal_id: int
    description: str
    measure: Optional[str]
    target: Optional[str]
    status: str
    sort_order: int

    class Config:
        from_attributes = True


class GoalCreate(BaseModel):
    treatment_plan_id: int
    title: str
    description: Optional[str] = None
    status: str = "active"
    sort_order: int = 0


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    sort_order: Optional[int] = None


class GoalOut(BaseModel):
    id: int
    treatment_plan_id: int
    title: str
    description: Optional[str]
    status: str
    sort_order: int

    class Config:
        from_attributes = True


class PlanCreate(BaseModel):
    client_id: int
    version: int = 1
    status: str = "draft"
    created_by: Optional[int] = None


class PlanUpdate(BaseModel):
    status: Optional[str] = None
    version: Optional[int] = None


class PlanOut(BaseModel):
    id: int
    client_id: int
    version: int
    status: str
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
        