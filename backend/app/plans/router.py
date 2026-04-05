from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.clients import repo as clients_repo
from app.core.deps import get_current_user, assert_client_access
from . import repo
from .schemas import (
    PlanCreate, PlanUpdate, PlanOut,
    GoalCreate, GoalUpdate, GoalOut,
    ObjectiveCreate, ObjectiveUpdate, ObjectiveOut,
    InterventionCreate, InterventionUpdate, InterventionOut
)

router = APIRouter()


# Treatment Plans
@router.post("/", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
def create_plan(payload: PlanCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.create_plan(db, payload.model_dump())


@router.get("/client/{client_id}", response_model=list[PlanOut])
def list_plans(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = clients_repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)
    return repo.list_plans_by_client(db, client_id)


@router.get("/{plan_id}", response_model=PlanOut)
def get_plan(plan_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    plan = repo.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    client = clients_repo.get_client(db, plan["client_id"])
    assert_client_access(client, current_user)
    return plan


@router.patch("/{plan_id}", response_model=PlanOut)
def update_plan(plan_id: int, payload: PlanUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    plan = repo.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    client = clients_repo.get_client(db, plan["client_id"])
    assert_client_access(client, current_user)
    updated = repo.update_plan(db, plan_id, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    plan = repo.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    client = clients_repo.get_client(db, plan["client_id"])
    assert_client_access(client, current_user)
    ok = repo.delete_plan(db, plan_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Plan not found")


# Goals
@router.post("/goals/", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.create_goal(db, payload.model_dump())


@router.get("/goals/plan/{plan_id}", response_model=list[GoalOut])
def list_goals(plan_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.list_goals_by_plan(db, plan_id)


@router.get("/goals/{goal_id}", response_model=GoalOut)
def get_goal(goal_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    goal = repo.get_goal(db, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.patch("/goals/{goal_id}", response_model=GoalOut)
def update_goal(goal_id: int, payload: GoalUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    goal = repo.update_goal(db, goal_id, payload.model_dump())
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ok = repo.delete_goal(db, goal_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Goal not found")


# Objectives
@router.post("/objectives/", response_model=ObjectiveOut, status_code=status.HTTP_201_CREATED)
def create_objective(payload: ObjectiveCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.create_objective(db, payload.model_dump())


@router.get("/objectives/goal/{goal_id}", response_model=list[ObjectiveOut])
def list_objectives(goal_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.list_objectives_by_goal(db, goal_id)


@router.get("/objectives/{objective_id}", response_model=ObjectiveOut)
def get_objective(objective_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    obj = repo.get_objective(db, objective_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objective not found")
    return obj


@router.patch("/objectives/{objective_id}", response_model=ObjectiveOut)
def update_objective(objective_id: int, payload: ObjectiveUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    obj = repo.update_objective(db, objective_id, payload.model_dump())
    if not obj:
        raise HTTPException(status_code=404, detail="Objective not found")
    return obj


@router.delete("/objectives/{objective_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_objective(objective_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ok = repo.delete_objective(db, objective_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Objective not found")


# Interventions
@router.post("/interventions/", response_model=InterventionOut, status_code=status.HTTP_201_CREATED)
def create_intervention(payload: InterventionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.create_intervention(db, payload.model_dump())


@router.get("/interventions/objective/{objective_id}", response_model=list[InterventionOut])
def list_interventions(objective_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repo.list_interventions_by_objective(db, objective_id)


@router.get("/interventions/{intervention_id}", response_model=InterventionOut)
def get_intervention(intervention_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    intervention = repo.get_intervention(db, intervention_id)
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention not found")
    return intervention


@router.patch("/interventions/{intervention_id}", response_model=InterventionOut)
def update_intervention(intervention_id: int, payload: InterventionUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    intervention = repo.update_intervention(db, intervention_id, payload.model_dump())
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention not found")
    return intervention


@router.delete("/interventions/{intervention_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_intervention(intervention_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ok = repo.delete_intervention(db, intervention_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Intervention not found")