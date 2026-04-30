#!/usr/bin/env python3
"""
setup.py — MentAssist first-time setup script
Run from the repo root: python setup.py

Performs all steps required before the app is usable:
  1. Copy .env.example -> .env for mentassistdb and backend
  2. Generate a SECRET_KEY and inject it into backend/.env
  3. Generate TLS certificates (platform-appropriate script)
  4. docker compose up --build
  5. Wait for containers and print verification instructions

Requires: Python 3.8+, Docker Desktop running, OpenSSL in PATH
"""

import os
import platform
import secrets
import shutil
import subprocess
import sys
import time

# ======== Colour helpers ===============================

def green(msg: str) -> str:
    return f"\033[32m{msg}\033[0m" if sys.stdout.isatty() else msg

def yellow(msg: str) -> str:
    return f"\033[33m{msg}\033[0m" if sys.stdout.isatty() else msg

def red(msg: str) -> str:
    return f"\033[31m{msg}\033[0m" if sys.stdout.isatty() else msg

def step(msg: str) -> None:
    print(f"\n{yellow('==>')} {msg}")

def ok(msg: str) -> None:
    print(green(f"  ✓ {msg}"))

def fail(msg: str) -> None:
    print(red(f"  ✗ {msg}"), file=sys.stderr)

# ============= Helpers ==================================

def repo_root() -> str:
    """Return the absolute path of the directory this script lives in."""
    return os.path.dirname(os.path.abspath(__file__))

def copy_env(example: str, target: str) -> None:
    """Copy example -> target only if target doesn't already exist."""
    if os.path.exists(target):
        ok(f"{target} already exists — skipping")
        return
    shutil.copy2(example, target)
    ok(f"Created {target}")

def inject_secret_key(env_path: str) -> None:
    """Replace the placeholder SECRET_KEY value with a generated one."""
    key = secrets.token_hex(32)
    with open(env_path, "r") as f:
        content = f.read()

    if f"SECRET_KEY={key}" in content:
        ok("SECRET_KEY already set — skipping")
        return

    # Replace any line that starts with SECRET_KEY=
    lines = content.splitlines(keepends=True)
    new_lines = []
    replaced = False
    for line in lines:
        if line.startswith("SECRET_KEY="):
            new_lines.append(f"SECRET_KEY={key}\n")
            replaced = True
        else:
            new_lines.append(line)

    if not replaced:
        new_lines.append(f"\nSECRET_KEY={key}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)

    ok(f"SECRET_KEY injected into {env_path}")

def run(cmd: list, **kwargs) -> subprocess.CompletedProcess:
    """Run a command, stream output, and raise on non-zero exit."""
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    return subprocess.run(cmd, check=True, **kwargs)

# ============= Platform detection ===================================

def detect_os() -> str:
    """Return 'windows', 'linux', or 'darwin'."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    if system == "darwin":
        return "darwin"
    return "linux"

# =========== Certificate generation ==================================

# Try to locate openssl.cnf on Windows relative to the openssl binary.
def find_openssl_cnf() -> str | None:
    openssl_bin = shutil.which("openssl")
    if not openssl_bin:
        return None
 
    # e.g. C:\Program Files\Git\usr\bin\openssl.exe
    #   -> base = C:\Program Files\Git
    bin_dir = os.path.dirname(openssl_bin)           # \usr\bin
    usr_dir = os.path.dirname(bin_dir)               # \usr
    base    = os.path.dirname(usr_dir)               # repo root / install root
 
    candidates = [
        os.path.join(usr_dir,  "ssl", "openssl.cnf"),           # Git for Windows
        os.path.join(base,     "ssl", "openssl.cnf"),
        os.path.join(base,     "Library", "ssl", "openssl.cnf"), # Miniconda
        r"C:\Program Files\Git\usr\ssl\openssl.cnf",
        r"C:\ProgramData\Miniconda3\Library\ssl\openssl.cnf",
    ]
    return next((p for p in candidates if os.path.exists(p)), None)


def generate_certs_windows(root: str) -> None:
    ps1 = os.path.join(root, "ops", "scripts", "generate-certs.ps1")
    if not os.path.exists(ps1):
        fail(f"Expected PowerShell cert script not found: {ps1}")
        sys.exit(1)
 
    env = os.environ.copy()
 
    # Pre-detect OPENSSL_CONF so the subprocess doesn't have to.
    # This is Windows-specific: OpenSSL bundled with Git for Windows or
    # Miniconda doesn't auto-locate its config file in a subprocess environment.
    if not env.get("OPENSSL_CONF"):
        cnf = find_openssl_cnf()
        if cnf:
            env["OPENSSL_CONF"] = cnf
            ok(f"OPENSSL_CONF set to: {cnf}")
        else:
            fail("Could not locate openssl.cnf automatically.")
            print(red(
                "\n  Set it manually before running setup.py:\n"
                "    $env:OPENSSL_CONF = \"C:\\<your-path>\\openssl.cnf\"\n"
                "    python setup.py\n"
                "\n  Common paths:\n"
                "    C:\\Program Files\\Git\\usr\\ssl\\openssl.cnf\n"
                "    C:\\ProgramData\\Miniconda3\\Library\\ssl\\openssl.cnf\n"
                "\n  See the README for more details."
            ), file=sys.stderr)
            sys.exit(1)
 
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1],
        cwd=root,
        env=env,  # pass the enriched environment explicitly
    )
    if result.returncode != 0:
        fail("Certificate generation failed.")
        sys.exit(1)
 
    ok("TLS certificates generated")


def generate_certs_unix(root: str) -> None:
    sh = os.path.join(root, "ops", "scripts", "generate-certs.sh")
    if not os.path.exists(sh):
        fail(f"Expected bash cert script not found: {sh}")
        sys.exit(1)

    # Ensure the script is executable
    os.chmod(sh, 0o755)

    result = subprocess.run(["bash", sh], cwd=root)
    if result.returncode != 0:
        fail("Certificate generation failed.")
        print(red(
            "\n  Ensure OpenSSL is installed:\n"
            "    macOS:          brew install openssl\n"
            "    Debian/Ubuntu:  sudo apt install openssl\n"
        ), file=sys.stderr)
        sys.exit(1)

# =========== Docker ==================================================

def check_docker(root: str) -> None:
    """Verify Docker daemon is reachable before we try to use it."""
    result = subprocess.run(
        ["docker", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=root,
    )
    if result.returncode != 0:
        fail("Docker daemon is not running. Start Docker Desktop and retry.")
        sys.exit(1)
    ok("Docker daemon is running")

def docker_compose_up(root: str) -> None:
    run(["docker", "compose", "up", "--build", "-d"], cwd=root)

def wait_for_containers(root: str, timeout: int = 60) -> None:
    """Poll until all compose services report as running, or timeout."""
    print(f"  Waiting for containers (up to {timeout}s)...", end="", flush=True)
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = subprocess.run(
            ["docker", "compose", "ps", "--status", "running", "--quiet"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        running = [l for l in result.stdout.strip().splitlines() if l]

        all_result = subprocess.run(
            ["docker", "compose", "ps", "--quiet"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        all_services = [l for l in all_result.stdout.strip().splitlines() if l]

        if all_services and len(running) >= len(all_services):
            print(" done.")
            return
        print(".", end="", flush=True)
        time.sleep(3)

    print("")
    fail("Timed out waiting for containers. Run `docker compose ps` to diagnose.")
    sys.exit(1)

# ========== Main ================================================================

def main() -> None:
    root = repo_root()
    os_name = detect_os()

    print(f"\nMentAssist Setup  |  detected OS: {platform.system()}")
    print("=" * 50)

    #  Step 1: .env files
    step("Step 1/4 — Copying .env files")
    copy_env(
        os.path.join(root, "mentassistdb", ".env.example"),
        os.path.join(root, "mentassistdb", ".env"),
    )
    copy_env(
        os.path.join(root, "backend", ".env.example"),
        os.path.join(root, "backend", ".env"),
    )

    #  Step 2: SECRET_KEY 
    step("Step 2/4 — Generating SECRET_KEY")
    inject_secret_key(os.path.join(root, "backend", ".env"))

    #  Step 3: TLS certificates 
    step("Step 3/4 — Generating TLS certificates")
    if os_name == "windows":
        generate_certs_windows(root)
    else:
        generate_certs_unix(root)

    #  Step 4: Docker 
    step("Step 4/4 — Building and starting Docker containers")
    check_docker(root)
    docker_compose_up(root)
    wait_for_containers(root)

    #  Done 
    print(f"\n{green('=' * 50)}")
    print(green("  MentAssist is ready!"))
    print(green("=" * 50))
    print("\n  Next steps:")
    print("    - Verify services:     docker compose ps")
    print("    - Backend API docs:    http://localhost:8000/docs")
    print("    - Open app:            https://localhost")
    print("\n  Seed accounts:")
    print("    counselor1@mentassist.com  /  Mentor123!  (counselor)")
    print("    counselor2@mentassist.com  /  Mentor123!  (counselor)")
    print("\n  To reset everything:   docker compose down -v && python setup.py\n")

if __name__ == "__main__":
    main()
