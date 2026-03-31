BEGIN;

-- users (counselor, admin)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('counselor','admin')),
  first_name TEXT,
  last_name TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','disabled')),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- table for clients & client data
CREATE TABLE clients (
  id SERIAL PRIMARY KEY,
  counselor_id INT NOT NULL REFERENCES users(id),
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  dob DATE,
  primary_diagnosis TEXT,
  primary_concerns TEXT,
  therapy_focus TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_clients_counselor ON clients(counselor_id);

-- appointment schema
CREATE TABLE appointments (
  id SERIAL PRIMARY KEY,
  client_id INT NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  scheduled_at TIMESTAMPTZ NOT NULL,
  location TEXT,
  created_by INT REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_appointments_client_time ON appointments(client_id, scheduled_at);

-- table for treatment plan data
CREATE TABLE treatment_plans (
  id SERIAL PRIMARY KEY,
  client_id INT NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  version INT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft','final','archived')),
  needs JSONB NOT NULL DEFAULT '[]',
  media JSONB NOT NULL DEFAULT '[]',
  created_by INT REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (client_id, version)
);

CREATE INDEX idx_treatment_plans_client ON treatment_plans(client_id);

-- treatment goals
CREATE TABLE treatment_goals (
  id SERIAL PRIMARY KEY,
  treatment_plan_id INT NOT NULL REFERENCES treatment_plans(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  sort_order INT DEFAULT 0
);

CREATE INDEX idx_goals_plan ON treatment_goals(treatment_plan_id);

-- treatment objectives
CREATE TABLE goal_objectives (
  id SERIAL PRIMARY KEY,
  goal_id INT NOT NULL REFERENCES treatment_goals(id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  measure TEXT,
  target TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  sort_order INT DEFAULT 0
);

CREATE INDEX idx_objectives_goal ON goal_objectives(goal_id);

-- excercises & intervention tactics
CREATE TABLE objective_interventions (
  id SERIAL PRIMARY KEY,
  objective_id INT NOT NULL REFERENCES goal_objectives(id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  frequency TEXT,
  responsible TEXT,
  sort_order INT DEFAULT 0
);

CREATE INDEX idx_interventions_objective ON objective_interventions(objective_id);

-- session notes
CREATE TABLE session_notes (
  id SERIAL PRIMARY KEY,
  client_id INT NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  appointment_id INT REFERENCES appointments(id) ON DELETE SET NULL,
  note_text TEXT NOT NULL,
  created_by INT REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_notes_client_time ON session_notes(client_id, created_at);

-- audit logs
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id INT,
  ts TIMESTAMPTZ DEFAULT now(),
  details JSONB
);

CREATE INDEX idx_audit_user_time ON audit_log(user_id, ts);

-- resource library
CREATE TABLE resources (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  type TEXT NOT NULL,
  tags JSONB NOT NULL DEFAULT '[]',
  file_name TEXT,
  mime_type TEXT,
  file_data BYTEA,
  created_by INT REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_resources_created_by ON resources(created_by);

COMMIT;