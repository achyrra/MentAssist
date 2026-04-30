#!/usr/bin/env bash
# generate-certs.sh
# Generates a self-signed TLS certificate for local development.
# Requires OpenSSL.
# Run once after cloning the repo, or any time the cert expires.
#
# Usage: bash ops/scripts/generate-certs.sh
#   (or from repo root as called by setup.py)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CERTS_DIR="$SCRIPT_DIR/../nginx/certs"

# Create certs directory if it doesn't exist
mkdir -p "$CERTS_DIR"

CERT_PATH="$CERTS_DIR/cert.pem"
KEY_PATH="$CERTS_DIR/key.pem"

# Check if OpenSSL is available
if ! command -v openssl &>/dev/null; then
    echo "ERROR: OpenSSL not found. Install it via your package manager:" >&2
    echo "  macOS:  brew install openssl" >&2
    echo "  Debian/Ubuntu: sudo apt install openssl" >&2
    exit 1
fi

echo "Generating self-signed certificate for localhost..."

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$KEY_PATH" \
    -out "$CERT_PATH" \
    -subj "/CN=localhost" \
    -addext "subjectAltName=IP:127.0.0.1,DNS:localhost"

echo ""
echo "Done. Certificate valid for 365 days."
echo "  cert: $CERT_PATH"
echo "  key:  $KEY_PATH"
