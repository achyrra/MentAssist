from fastapi import APIRouter, HTTPException, Depends, status, Response, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user, assert_client_access
from .schemas import ClientCreate, ClientUpdate, ClientOut
from . import repo
from app.notes import repo as notes_repo
from app.notes.schemas import ClientNoteCreate, ClientNoteOut
from app.plans import repo as plans_repo
from pydantic import BaseModel
from typing import Any
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT
import io
from datetime import date

router = APIRouter()


class PlanPayload(BaseModel):
    needs: list[Any] = []
    media: list[Any] = []


def _calc_age(dob) -> str:
    if not dob:
        return "—"
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return str(age)


def _build_plan_pdf(client: dict, plan: dict, counselor: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
    )

    sage       = colors.HexColor("#4E7361")
    sage_light = colors.HexColor("#7A9B8A")
    cream      = colors.HexColor("#F5F0E8")
    divider    = colors.HexColor("#E0D8CC")
    charcoal   = colors.HexColor("#2C2C2C")
    mid        = colors.HexColor("#6B6B6B")
    light      = colors.HexColor("#A0A0A0")

    styles = getSampleStyleSheet()

    label_style = ParagraphStyle(
        "label", fontSize=7, textColor=sage_light, spaceAfter=2,
        fontName="Helvetica-Bold", leading=10,
    )
    brand_style = ParagraphStyle(
        "brand", fontSize=7, textColor=sage_light, spaceAfter=4,
        fontName="Helvetica-Bold", leading=10,
    )
    section_label_style = ParagraphStyle(
        "sectionlabel", fontSize=7, textColor=sage, spaceAfter=4,
        fontName="Helvetica-Bold", leading=10,
    )
    client_info_style = ParagraphStyle(
        "clientinfo", fontSize=9, textColor=charcoal, spaceAfter=2,
        fontName="Helvetica", leading=14,
    )
    need_title_style = ParagraphStyle(
        "needtitle", fontSize=11, textColor=charcoal, spaceAfter=2,
        fontName="Helvetica-Bold", leading=14,
    )
    need_label_style = ParagraphStyle(
        "needlabel", fontSize=7, textColor=sage, spaceAfter=2,
        fontName="Helvetica-Bold", leading=10,
    )
    body_style = ParagraphStyle(
        "body", fontSize=9, textColor=charcoal, spaceAfter=3,
        fontName="Helvetica", leading=14,
    )
    objective_style = ParagraphStyle(
        "objective", fontSize=9, textColor=charcoal, spaceAfter=3,
        fontName="Helvetica", leading=14, leftIndent=14,
    )
    intervention_style = ParagraphStyle(
        "intervention", fontSize=9, textColor=charcoal, spaceAfter=3,
        fontName="Helvetica", leading=14, leftIndent=14,
    )
    footer_style = ParagraphStyle(
        "footer", fontSize=7, textColor=light,
        fontName="Helvetica", leading=10,
    )
    empty_style = ParagraphStyle(
        "empty", fontSize=9, textColor=light,
        fontName="Helvetica", leading=14,
    )

    story = []
    today_str = date.today().strftime("%B %d, %Y")
    dob = client.get("dob")
    dob_str = dob.strftime("%B %d, %Y") if dob else "—"
    age_str = _calc_age(dob)
    client_name = f"{client['first_name']} {client['last_name']}"
    counselor_name = f"{counselor.get('first_name', '')} {counselor.get('last_name', '')}".strip() or counselor.get('email', '')

    story.append(Paragraph("MENTASSIST · TREATMENT PLAN", brand_style))
    story.append(HRFlowable(width="100%", thickness=2, color=sage, spaceAfter=8))
    story.append(Paragraph("CLIENT INFORMATION", section_label_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=divider, spaceAfter=6))
    story.append(Paragraph(f"<b>Name:</b> {client_name}", client_info_style))
    story.append(Paragraph(f"<b>Date of Birth:</b> {dob_str} (Age {age_str})", client_info_style))
    story.append(Paragraph(f"<b>Date:</b> {today_str}", client_info_style))
    story.append(Spacer(1, 16))

    needs = plan.get("needs") or []
    if not needs:
        story.append(Paragraph("No treatment needs have been added.", empty_style))
    else:
        for i, need in enumerate(needs):
            if i > 0:
                story.append(HRFlowable(width="100%", thickness=0.5, color=divider, spaceBefore=12, spaceAfter=12))
            story.append(Paragraph(f"TREATMENT NEED {i + 1}", need_label_style))
            story.append(Paragraph(need.get("title", "Untitled"), need_title_style))
            goal = need.get("goal")
            if goal:
                story.append(Spacer(1, 4))
                story.append(Paragraph("TREATMENT GOAL", label_style))
                story.append(Paragraph(goal, body_style))
            objectives = need.get("objectives") or []
            if objectives:
                story.append(Spacer(1, 4))
                story.append(Paragraph("SHORT-TERM OBJECTIVES", label_style))
                for oi, obj in enumerate(objectives):
                    story.append(Paragraph(f"{oi + 1}.  {obj}", objective_style))
            interventions = need.get("interventions") or []
            if interventions:
                story.append(Spacer(1, 4))
                story.append(Paragraph("INTERVENTIONS", label_style))
                for iv in interventions:
                    story.append(Paragraph(f"•  {iv}", intervention_style))

    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="100%", thickness=0.5, color=divider, spaceAfter=6))
    story.append(Paragraph(
        f"Prepared by: {counselor_name}&nbsp;&nbsp;&nbsp;&nbsp;MentAssist Therapy Platform · Confidential",
        footer_style,
    ))

    doc.build(story)
    return buffer.getvalue()


@router.post("", status_code=201, response_model=ClientOut)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    data = payload.model_dump()
    data["counselor_id"] = data.get("counselor_id") or current_user["id"]
    return repo.create_client(db, data)


@router.get("", response_model=list[ClientOut])
def list_clients(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "admin":
        return repo.list_clients(db, counselor_id=None, limit=limit, offset=offset)
    return repo.list_clients(db, counselor_id=current_user["id"], limit=limit, offset=offset)


@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)
    return client


@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)

    updated = repo.update_client(db, client_id, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)

    deleted = repo.delete_client(db, client_id, user_id=current_user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")


@router.get("/{client_id}/plan")
def get_plan(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)
    plan = plans_repo.get_plan_by_client(db, client_id)
    if not plan:
        return {"needs": [], "media": []}
    return {"needs": plan["needs"], "media": plan["media"]}


@router.put("/{client_id}/plan")
def save_plan(client_id: int, payload: PlanPayload, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)
    plan = plans_repo.upsert_plan(db, client_id, payload.needs, payload.media, user_id=current_user["id"])
    return {"needs": plan["needs"], "media": plan["media"]}


@router.get("/{client_id}/plan/export")
def export_plan(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)
    plan = plans_repo.get_plan_by_client(db, client_id)
    if not plan:
        raise HTTPException(status_code=404, detail="No plan found for client")
    pdf_bytes = _build_plan_pdf(client, plan, current_user)
    filename = f"{client['first_name']}-{client['last_name']}-treatment-plan.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/{client_id}/notes", response_model=ClientNoteOut, status_code=status.HTTP_201_CREATED)
def create_client_note(client_id: int, payload: ClientNoteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)
    note = notes_repo.create_note(db, {
        "client_id": client_id,
        "note_text": payload.content,
        "appointment_id": None,
        "created_by": current_user["id"]
    })
    return {"id": note["id"], "content": note["note_text"], "created_at": note["created_at"]}


@router.get("/{client_id}/notes", response_model=list[ClientNoteOut])
def list_client_notes(
    client_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    assert_client_access(client, current_user)
    notes = notes_repo.list_notes_by_client(db, client_id, limit=limit, offset=offset)
    return [{"id": n["id"], "content": n["note_text"], "created_at": n["created_at"]} for n in notes]