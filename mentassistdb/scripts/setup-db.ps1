# Be sure to run from repo root!: .\scripts\setup-db.ps1 

docker compose up -d

Start-Sleep -Seconds 2

Get-Content .\db\schema.sql | docker exec -i mentassist-db psql -U postgres_admin -d mentassist_app
Get-Content .\db\roles.sql  | docker exec -i mentassist-db psql -U postgres_admin -d mentassist_app

# When seed is added in the directory, will run & fill with example treatment plans.
if (Test-Path .\db\seed.sql) {
  Get-Content .\db\seed.sql | docker exec -i mentassist-db psql -U postgres_admin -d mentassist_app
}

Write-Host "✅ MentAssist DB ready on localhost:5432 (DB=mentassist_app)"