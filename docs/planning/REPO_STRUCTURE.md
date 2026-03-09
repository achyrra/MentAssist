# MentAssist — Target Repository Structure
# Generated as a refactoring guide. Annotations explain moves and reasoning.
# legend: [MOVE] = exists, relocate it | [NEW] = needs to be created | [KEEP] = already correct | [RENAME] = rename only

# Current as of 3/8/26

mentassist/
│
├── README.md                          # [KEEP] — update paths inside it
├── .gitignore                         # [KEEP] — already at root, correct
├── docker-compose.yml                 # [MOVE] was inside mentassistdb/ — compose belongs at repo root
│
├── ops/                               # [NEW] security/infra-owned 
│   ├── nginx/
│   │   ├── nginx.conf                 # [NEW] 
│   │   └── sites-enabled/
│   │       └── app.conf               # [NEW] 
│   └── scripts/
│       ├── setup-db.ps1               # [MOVE] was at mentassistdb/scripts/setup-db.ps1
│       ├── backup_db.sh               # [NEW] — stub, implement in S4
│       └── restore_db.sh              # [NEW] — stub, implement in S4
│
├── backend/
│   ├── Dockerfile                     # [KEEP] — already correct
│   ├── .dockerignore                  # [KEEP] — already correct
│   ├── .env.example                   # [NEW] — was missing
│   ├── requirements.txt               # [KEEP]
│   │
│   └── app/                           # [NEW] wrap everything under app/ — fixes import paths
│       ├── main.py                    # [MOVE] was at backend/main.py
│       │
│       ├── api/
│       │   ├── __init__.py            # [KEEP]
│       │   └── v1/
│       │       ├── __init__.py        # [KEEP]
│       │       └── router.py          # [KEEP] — update import paths after move
│       │
│       ├── core/
│       │   ├── __init__.py            # [NEW] was missing
│       │   └── config.py             # [MOVE] was at backend/core/config.py
│       │
│       ├── db/
│       │   ├── __init__.py            # [NEW] was missing
│       │   └── session.py             # [MOVE] was at backend/db/session.py
│       │
│       ├── clients/
│       │   ├── __init__.py            # [KEEP]
│       │   ├── router.py              # [MOVE] was at backend/clients/router.py
│       │   ├── repo.py                # [MOVE] was at backend/clients/repo.py
│       │   └── schemas.py             # [MOVE] was at backend/clients/schemas.py
│       │
│       ├── appointments/
│       │   ├── __init__.py            # [KEEP]
│       │   ├── router.py              # [MOVE] was at backend/appointments/router.py
│       │   ├── repo.py                # [MOVE] was at backend/appointments/repo.py
│       │   └── schemas.py             # [MOVE] was at backend/appointments/schemas.py
│       │
│       ├── users/
│       │   ├── __init__.py            # [KEEP]
│       │   ├── router.py              # [MOVE] was at backend/users/router.py
│       │   ├── repo.py                # [MOVE] was at backend/users/repo.py
│       │   └── schemas.py             # [MOVE] was at backend/users/schemas.py
│       │
│       ├── notes/                     # [NEW] session notes module — S2.R1 work
│       │   ├── __init__.py
│       │   ├── router.py
│       │   ├── repo.py
│       │   └── schemas.py
│       │
│       └── treatment_plans/           # [NEW] treatment plan module — S2.R3 work
│           ├── __init__.py
│           ├── router.py
│           ├── repo.py
│           └── schemas.py
│
│   └── tests/                         # [NEW] — empty now, needed for S4
│       ├── __init__.py
│       ├── test_clients.py
│       ├── test_appointments.py
│       └── test_notes.py
│
├── frontend/                          # [NEW] frontend team's home
│   ├── Dockerfile                     # [NEW] 
│   ├── .dockerignore                  # [NEW] — frontend team to add
│   ├── public/                        # [NEW] — frontend team to populate
│   └── src/                           # [NEW] — frontend team to populate
│
├── db/                                # [RENAME] was mentassistdb/ — cleaner, aligns with template
│   ├── .env.example                   # [MOVE] was at mentassistdb/.env.example
│   ├── .gitignore                     # [KEEP] — already ignores .env correctly
│   └── db/
│       ├── schema.sql                 # [KEEP]
│       └── roles.sql                  # [KEEP]
│
└── docs/                              # [NEW] replaces "MentAssist Docs/" — consistent naming
    ├── SETUP_DB.md                    # [MOVE] was at MentAssist Docs/SETUP_DB.md
    ├── SERVER_SETUP.md                # [MOVE] was at MentAssist Docs/SERVER_SETUP.md
    ├── architecture.md                # [NEW] written doc form of the docx — easier to version control
    ├── api.md                         # [NEW] endpoint reference — stub for now, fill as routes grow
    └── planning/                      # [NEW] non-code planning artifacts
        ├── Product_Roadmap.docx       # [MOVE] was at repo root
        ├── Product_Vision.docx        # [MOVE] was at repo root
        ├── User_Stories.docx          # [MOVE] was at repo root
        ├── Sample_Treatment_Plan.docx # [MOVE] was at repo root
        └── workflows.xlsx             # [MOVE] was at repo root
