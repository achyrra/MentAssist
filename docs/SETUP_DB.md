# MentAssist Database Setup

This document explains how to run a local PostgreSQL database strictly for dev. 

Prerequisites: 
  - Docker Desktop installed & running.
  - Windows PowerShell

Setup Instructions: 
  1. Download & install the zipped package "MentAssist"
  2. Access the folder directory using the terminal.
     - you can do this from any given code editor or Windows PowerShell application itself.
  3. Using the terminal, run 'docker compose up -d'
  4. Using the terminal, you can now run 'copy .env.example .env'
     - ".env.example" is used to set a baseline for .env, hence why we copy & let the provided powershell script run. 
  5. Run '.\scripts\setup-db.ps1'
     - if successful, one should see "MentAssist DB ready on localhost:5432 (DB=mentassist_app)

Veriification Instructions: 
  1. To list the provided tables in the terminal, run 'docker exec -it mentassist-db psql -U postgres_admin -d mentassist_app -c "\dt"'
     - we should expect to see a list of nine different tables

To Stop the Database: 
  Run 'docker compose down -v'
