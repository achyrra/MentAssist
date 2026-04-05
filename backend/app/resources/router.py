from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from . import repo
import json
import io

router = APIRouter()


@router.get("")
def list_resources(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    rows = repo.list_resources(db, limit=limit, offset=offset)
    return [
        {
            "id":       str(r["id"]),
            "title":    r["title"],
            "type":     r["type"],
            "tags":     r["tags"] if isinstance(r["tags"], list) else json.loads(r["tags"]),
            "fileName": r["file_name"],
            "mimeType": r["mime_type"],
        }
        for r in rows
    ]


@router.post("", status_code=201)
async def create_resource(
    title:        str        = Form(...),
    type:         str        = Form(...),
    tags:         str        = Form("[]"),
    file:         UploadFile = File(...),
    db:           Session    = Depends(get_db),
    current_user: dict       = Depends(get_current_user),
):
    file_data = await file.read()
    tags_list = json.loads(tags) if tags else []
    row = repo.create_resource(db, {
        "title":      title,
        "type":       type,
        "tags":       tags_list,
        "file_name":  file.filename,
        "mime_type":  file.content_type,
        "file_data":  file_data,
        "created_by": current_user["id"],
    })
    return {
        "id":       str(row["id"]),
        "title":    row["title"],
        "type":     row["type"],
        "tags":     row["tags"] if isinstance(row["tags"], list) else json.loads(row["tags"]),
        "fileName": row["file_name"],
        "mimeType": row["mime_type"],
    }


@router.get("/{resource_id}/download")
def download_resource(resource_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    r = repo.get_resource(db, resource_id)
    if not r:
        raise HTTPException(status_code=404, detail="Resource not found")
    if not r["file_data"]:
        raise HTTPException(status_code=404, detail="No file data for this resource")
    return StreamingResponse(
        io.BytesIO(bytes(r["file_data"])),
        media_type=r["mime_type"] or "application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={r['file_name']}"},
    )


@router.delete("/{resource_id}", status_code=204)
def delete_resource(resource_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    deleted = repo.delete_resource(db, resource_id, user_id=current_user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found")