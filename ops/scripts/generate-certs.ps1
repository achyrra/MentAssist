# generate-certs.ps1
# Generates a self-signed TLS certificate for local development.
# Requires OpenSSL.
# Run once after cloning the repo, or any time the cert expires.
#
# Usage: .\ops\scripts\generate-certs.ps1
#   (or from repo root as called by setup.py)

$certsDir = "$PSScriptRoot\..\nginx\certs"

# Create certs directory if it doesn't exist
if (-not (Test-Path $certsDir)) {
    New-Item -ItemType Directory -Path $certsDir | Out-Null
}

$certPath = "$certsDir\cert.pem"
$keyPath  = "$certsDir\key.pem"

# Check if OpenSSL is available
if (-not (Get-Command openssl -ErrorAction SilentlyContinue)) {
    Write-Error "OpenSSL not found. Make sure Git for Windows or Miniconda is installed and in your PATH."
    exit 1
}

# Locate openssl.cnf relative to the openssl binary
$opensslBin = (Get-Command openssl).Source
$opensslBase = Split-Path (Split-Path $opensslBin -Parent) -Parent
if ($env:OPENSSL_CONF -and (Test-Path $env:OPENSSL_CONF)) {
    $cnfPath = $env:OPENSSL_CONF
} else {
    $cnfCandidates = @(
        "$opensslBase\ssl\openssl.cnf",
        "$opensslBase\Library\ssl\openssl.cnf",
        "C:\Program Files\Git\usr\ssl\openssl.cnf"
    )
    $cnfPath = $cnfCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $cnfPath) {
        Write-Error "Could not locate openssl.cnf. Set OPENSSL_CONF manually and re-run."
        exit 1
    }
}
$env:OPENSSL_CONF = $cnfPath
Write-Host "Using OpenSSL config: $cnfPath"

Write-Host "Generating self-signed certificate for localhost..."

openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
    -keyout $keyPath `
    -out $certPath `
    -subj "/CN=localhost" `
    -addext "subjectAltName=IP:127.0.0.1,DNS:localhost"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Done. Certificate valid for 365 days." -ForegroundColor Green
    Write-Host "  cert: $certPath"
    Write-Host "  key:  $keyPath"
} else {
    Write-Error "Certificate generation failed."
    exit 1
}