from fastapi import FastAPI
from sqlalchemy import text
from db.session import engine

app = FastAPI(title="MentAssist API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-ping")
def db_ping():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}