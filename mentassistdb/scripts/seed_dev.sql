-- DEV ONLY SEED DATA
INSERT INTO users (id, email, password_hash, role) VALUES
  (1, 'counselor1@mentassist.com', '$2b$12$kXlwBb//4OTjXXKDn6RZxuoEIC0D80/dWYEvOQk.oGref32UKRAhu', 'counselor'), -- replace $realhash with hash generated during setup (see README)
  (2, 'counselor2@mentassist.com', '$2b$12$kXlwBb//4OTjXXKDn6RZxuoEIC0D80/dWYEvOQk.oGref32UKRAhu', 'counselor')
ON CONFLICT (id) DO UPDATE SET password_hash = EXCLUDED.password_hash;

INSERT INTO clients (id, counselor_id, first_name, last_name, dob) VALUES
  (1, 2, 'Maya',   'Johnson', '1990-03-14'),
  (2, 2, 'Daniel', 'Reyes',   '1985-11-22'),
  (3, 2, 'Priya',  'Nair',    '1998-07-09')
ON CONFLICT DO NOTHING;