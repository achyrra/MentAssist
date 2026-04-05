# MentAssist
Please see "SETUP_DB.md" for instructions on setting up the database.

# Documentation
- Folder "MentAssist Docs" stores individual files documenting architecture and project planning.
- Any future changes will be documented and uploaded to the same folder.

# Dev Env Setup
1. Clone repo at https://github.com/achyrra/MentAssist.git
2. In terminal use the following commands:
    - `cp mentassistdb\.env.example mentassistdb\.env`
        - Do not commit this file
    - `cp backend\.env.example backend\.env`
        - Do not commit this file
    - Generate a SECRET_KEY for `backend\.env`:
        - `python -c "import secrets; print(secrets.token_hex(32))"`
        - Copy the output and paste as `SECRET_KEY=<generated_value>`
    - Generate TLS certificates (NOTE: this is a Powershell script):
        - `.\ops\scripts\generate-certs.ps1`
        - This creates `ops/nginx/certs/cert.pem` and `key.pem` locally
        - Never commit these files
    - `docker compose up --build`
    - `docker compose ps`
3. Verify all services are running
4. Confirm backend docs are reachable at `http://localhost:8000/docs`
5. Open app at `https://localhost`
6. Login with seed accounts:

| Email | Password | Role |
|---|---|---|
| counselor1@mentassist.com | Mentor123! | counselor |
| counselor2@mentassist.com | Mentor123! | counselor |

# Seed Data
Counselor2 owns three seed clients: Maya Johnson, Daniel Reyes, and Priya Nair.

# Notes
- Seed hashes are pre-generated real bcrypt hashes -- no manual hash generation needed.
- Backend connects as `app_user` with password `app_password_change_me`.
- To fully reset the database: `docker compose down -v && docker compose up --build`
- If `generate-certs.ps1` fails to locate `openssl.cnf`, run the following instead, replacing the path with your actual OpenSSL config location:
    - `$env:OPENSSL_CONF = "C:\<your-path>\openssl.cnf"`
    - `.\ops\scripts\generate-certs.ps1`