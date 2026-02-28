@"
# MentAssist Backend Server Setup

## System Requirements

- Docker Desktop (running)
- Python 3.11 or newer
- PowerShell (Windows)
- Git (if cloning repository)

Verify Python version:
python --version

---

## Expected Project Structure

MentAssist/
│
├── backend/
│   ├── main.py
│   ├── api/
│   ├── clients/
│   ├── appointments/
│   └── venv/
│
└── mentassistdb/
    ├── docker-compose.yml
    ├── schema.sql
    └── .env

---

# 1. Database Setup

Navigate to the database folder:
cd mentassistdb

Create .env if missing:
copy .env.example .env

Start PostgreSQL container:
docker compose up -d

Verify container is running:
docker ps

You should see:
mentassist-db

Load schema (first run only):
Get-Content schema.sql | docker exec -i mentassist-db psql -U postgres_admin -d mentassist_app -v ON_ERROR_STOP=1

If successful, output includes:
BEGIN
CREATE TABLE
...
COMMIT

Database is ready.

---

# 2. Backend Setup

Navigate to backend:
cd ..\backend

Create virtual environment (first run only):
python -m venv venv

Activate environment:
.\venv\Scripts\activate

Install dependencies:
pip install fastapi uvicorn psycopg2-binary python-dotenv

Optional: generate requirements file:
pip freeze > requirements.txt

---

# 3. Verify Environment

Confirm interpreter and packages:
python -c "import fastapi; import uvicorn; print('ok')"

Expected output:
ok

---

# 4. Run the API Server

From inside backend with venv activated:
uvicorn main:app --reload

Expected terminal output:
Uvicorn running on http://127.0.0.1:8000

---

# 5. Access the API

Open browser and go to:

Base URL:
http://127.0.0.1:8000

Health endpoint:
http://127.0.0.1:8000/health

Versioned clients endpoint:
http://127.0.0.1:8000/api/v1/clients

Swagger UI:
http://127.0.0.1:8000/docs

ReDoc:
http://127.0.0.1:8000/redoc

---

# 6. Custom Port (Optional)

Run on a different port:
uvicorn main:app --reload --port 9000

Then access:
http://127.0.0.1:9000

---

# 7. Stop Services

Stop API server:
Press CTRL + C

Stop database:
docker compose down

---

# 8. Common Failure Modes

ModuleNotFoundError: fastapi
- Virtual environment not activated.

ModuleNotFoundError: appointments.router
- Router file missing or missing __init__.py.

Import warnings in VSCode
- Interpreter not set to:
backend\venv\Scripts\python.exe

Database connection failure
- Docker not running
- Wrong credentials in .env
- Schema not loaded

---

Status Checklist

Database running
Schema loaded
Virtual environment activated
Dependencies installed
Uvicorn running
Swagger UI accessible

This setup is reproducible on a clean machine if steps are followed exactly.
"@ | Out-File -Encoding UTF8 SERVER_SETUP.md