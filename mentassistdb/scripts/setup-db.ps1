# Be sure to run from repo root!: .\mentassistdb\scripts\setup-db.ps1

docker compose up -d

Start-Sleep -Seconds 5

Get-Content .\mentassistdb\db\schema.sql | docker exec -i mentassistdb psql -U postgres_admin -d mentassist_app
Get-Content .\mentassistdb\db\roles.sql  | docker exec -i mentassistdb psql -U postgres_admin -d mentassist_app

if (Test-Path .\mentassistdb\scripts\seed_dev.sql) {
  Get-Content .\mentassistdb\scripts\seed_dev.sql | docker exec -i mentassistdb psql -U postgres_admin -d mentassist_app
}

Write-Host "MentAssist DB ready on localhost:5432 (DB=mentassist_app)"
