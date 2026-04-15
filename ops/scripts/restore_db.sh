#!/usr/bin/env bash
# MentAssist PostgreSQL Restore Script
#
# Usage: ./ops/scripts/restore_db.sh --file <backup_file> [--confirm]
#
# Defaults (override via environment variables):
#   DB_CONTAINER    mentassistdb
#   DB_NAME         mentassist_app
#   DB_USER         postgres_admin
# =================================================================================

set -euo pipefail

# Default configurations
DB_CONTAINER="${DB_CONTAINER:-mentassistdb}"
DB_NAME="${DB_NAME:-mentassist_app}"
DB_USER="${DB_USER:-postgres_admin}"
 
BACKUP_FILE=""
CONFIRMED=false


# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --file)
      BACKUP_FILE="$2"
      shift 2
      ;;
    --confirm)
      CONFIRMED=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 --file <backup_file> [--confirm]"
      exit 1
      ;;
  esac
done


# Preflight checks
if [[ -z "$BACKUP_FILE" ]]; then
  echo "[ERROR] --file is required." >&2
  echo "Usage: $0 --file <backup_file> [--confirm]" >&2
  exit 1
fi
 
if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "[ERROR] Backup file not found: $BACKUP_FILE" >&2
  exit 1
fi
 
if ! command -v docker &>/dev/null; then
  echo "[ERROR] docker not found in PATH." >&2
  exit 1
fi
 
if ! docker inspect "$DB_CONTAINER" &>/dev/null; then
  echo "[ERROR] Container '$DB_CONTAINER' is not running." >&2
  exit 1
fi


# Confirmation gate
echo ""
echo "  ╔══════════════════════════════════════════════════════╗"
echo "  ║           ⚠  DESTRUCTIVE OPERATION  ⚠               ║"
echo "  ║                                                      ║"
echo "  ║  This will DROP and RECREATE '$DB_NAME'              ║"
echo "  ║  All current data will be permanently lost.          ║"
echo "  ║                                                      ║"
echo "  ║  Restore file: $(basename "$BACKUP_FILE")            ║"
echo "  ╚══════════════════════════════════════════════════════╝"
echo ""
 
if [[ "$CONFIRMED" != true ]]; then
  read -r -p "Type 'yes' to continue: " response
  if [[ "$response" != "yes" ]]; then
    echo "[restore] Aborted."
    exit 0
  fi
fi


# Terminate active connections to the database before dropping it
echo "[restore] Terminating active connections to '$DB_NAME'..."
docker exec "$DB_CONTAINER" psql -U "$DB_USER" -d postgres --no-password -c \
  "SELECT pg_terminate_backend(pid)
   FROM pg_stat_activity
   WHERE datname = '${DB_NAME}' AND pid <> pg_backend_pid();" \
  > /dev/null


# Drop and recreate the database
echo "[restore] Dropping database '$DB_NAME'..."
docker exec "$DB_CONTAINER" psql -U "$DB_USER" -d postgres --no-password \
  -c "DROP DATABASE IF EXISTS ${DB_NAME};"
 
echo "[restore] Recreating database '$DB_NAME'..."
docker exec "$DB_CONTAINER" psql -U "$DB_USER" -d postgres --no-password \
  -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"


# Restore from backup
echo "[restore] Restoring from $BACKUP_FILE ..."
 
gunzip -c "$BACKUP_FILE" | docker exec -i "$DB_CONTAINER" \
  psql -U "$DB_USER" -d "$DB_NAME" --no-password
 
echo "[restore] Restore complete. Database '$DB_NAME' is ready."