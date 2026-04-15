#!/usr/bin/env bash
# MentAssist PostgreSQL Backup Script
#
# Usage: ./ops/scripts/backup_db.sh [--retain-days N]
#
# Defaults (override via environment variables):
#   BACKUP_DIR      ./backups
#   RETAIN_DAYS     30
#   DB_CONTAINER    mentassistdb
#   DB_NAME         mentassist_app
#   DB_USER         postgres_admin
#
# Example (custom backup dir, keep 14 days):
#   BACKUP_DIR=/mnt/backups RETAIN_DAYS=14 ./ops/scripts/backup_db.sh
# ===================================================================================

set -euo pipefail

# Default configurations
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETAIN_DAYS="${RETAIN_DAYS:-30}"
DB_CONTAINER="${DB_CONTAINER:-mentassistdb}"
DB_NAME="${DB_NAME:-mentassist_app}"
DB_USER="${DB_USER:-postgres_admin}"
 
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/mentassist_${TIMESTAMP}.sql.gz"


# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --retain-days)
      RETAIN_DAYS="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--retain-days N]"
      exit 1
      ;;
  esac
done


# Preflight checks
if ! command -v docker &>/dev/null; then
  echo "[ERROR] docker not found in PATH." >&2
  exit 1
fi
 
if ! docker inspect "$DB_CONTAINER" &>/dev/null; then
  echo "[ERROR] Container '$DB_CONTAINER' is not running." >&2
  exit 1
fi
 
mkdir -p "$BACKUP_DIR"


# Dump
echo "[backup] Starting backup of '$DB_NAME' → $BACKUP_FILE"
 
docker exec "$DB_CONTAINER" \
  pg_dump -U "$DB_USER" -d "$DB_NAME" --no-password \
  | gzip > "$BACKUP_FILE"
 
echo "[backup] Done. $(du -sh "$BACKUP_FILE" | cut -f1) written."


# Retention: remove dumps older than RETAIN_DAYS
echo "[backup] Pruning backups older than ${RETAIN_DAYS} days..."
find "$BACKUP_DIR" -name "mentassist_*.sql.gz" -mtime "+${RETAIN_DAYS}" -delete
echo "[backup] Pruning complete."