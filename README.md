# MentAssist

Please see "SETUP_DB.md" for instructions on setting up the database. 

# Documentation
- Folder "MentAssist Docs" stores individual files documenting architecture and project planning.
- Any future changes will be documented and uploaded to the same folder.

# Dev Env Setup
1. Clone repo at https://github.com/achyrra/MentAssist.git
2. In terminal use following commands:
    - cp \mentassistdb\.env.example \mentassistdb\.env
        - Do not commit this new file
    - cp \backend\.env.example \backend\.env
        - Do not commit this new file
    - "import bcrypt; print(bcrypt.hashpw(b'password123', bcrypt.gensalt()).decode())" | Out-File -Encoding utf8 -FilePath hash.py
    - docker run --rm -v "${PWD}:/scripts" python:3.12-alpine sh -c "pip install bcrypt -q && python3 /scripts/hash.py"
        - Copy the generated $2b$12$... output and paste into \mentassistdb\scripts\seed_dev.sql in both user rows
    - Remove-Item hash.py
    - docker compose up --build
    - docker compose ps
4. Verify all services are running
5. Confirm backend docs are reachable (http://localhost/api/v1/docs)
6. Open app (http://localhost)
7. Login:
    - Email: counselor1@mentassist.com
    - Password: password123
8. Generate a hash for your backend/.env file via the following command in powershell:
    - python -c "import secrets; print(secrets.token_hex(32))"
    - Copy the output and paste as SECRET_KEY=<generated_value>
