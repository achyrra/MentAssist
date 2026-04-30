# MentAssist

A clinical counselor workflow tool for managing client profiles, appointment scheduling, session notes, and treatment plans.

---

## Prerequisites

Before running the setup script, ensure the following are installed:

| Requirement | Notes |
|---|---|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Must be running before setup |
| Python 3.8+ | Used to run `setup.py` |
| OpenSSL | Windows: ships with Git for Windows or Miniconda — macOS/Linux: pre-installed |

---

## Setup

1. Download and extract the source code from the provided zip, 
or Clone the repository:
    ```
    git clone https://github.com/achyrra/MentAssist.git
    cd MentAssist
    ```

2. Start Docker Desktop and wait until it is fully running.

3. From the repo root, run:
    ```
    python setup.py
    ```

---

## Verify

Once setup completes, confirm everything is running:

```
docker compose ps
```

All services should show a `running` status.

| Endpoint | URL |
|---|---|
| Backend API docs (Swagger UI) | http://localhost:8000/docs |
| Application | https://localhost |

> **Note:** Your browser will show a security warning for the self-signed TLS certificate. This is expected because the TLS certs are self-signed.

---

## Login

Use the following seed accounts to log in:

| Email | Password | Role |
|---|---|---|
| counselor1@mentassist.com | Mentor123! | counselor |
| counselor2@mentassist.com | Mentor123! | counselor |

`counselor2` owns three pre-seeded clients: Maya Johnson, Daniel Reyes, and Priya Nair.

---

## Reset

To fully wipe and re-run setup from scratch:

```
docker compose down -v
python setup.py
```

---

## Troubleshooting

### OpenSSL config not found (Windows)

If setup fails with `Could not locate openssl.cnf`, set `OPENSSL_CONF` manually in PowerShell before re-running:

```powershell
$env:OPENSSL_CONF = "C:\<your-path>\openssl.cnf"
python setup.py
```

Common paths:

| Installation | Path |
|---|---|
| Git for Windows | `C:\Program Files\Git\usr\ssl\openssl.cnf` |
| Miniconda | `C:\ProgramData\Miniconda3\Library\ssl\openssl.cnf` |

### Docker daemon not running

If setup fails with `Docker daemon is not running`, open Docker Desktop, wait for it to finish starting, then re-run `python setup.py`.

### Containers not reaching running state

If the script times out waiting for containers, check the logs:

```
docker compose ps
docker compose logs
```