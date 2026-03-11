from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine
from app.api.v1.router import router as v1_router

app = FastAPI(
    title="MentAssist API",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json",
    redoc_url="/api/v1/redoc",
    redirect_slashes=False
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-ping")
def db_ping():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}

app.include_router(v1_router, prefix="/api/v1")