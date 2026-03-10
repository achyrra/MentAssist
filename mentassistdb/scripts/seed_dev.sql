-- DEV ONLY SEED DATA
INSERT INTO users (id, email, password_hash, role) VALUES
  (1, 'counselor1@mentassist.com', '$realhash', 'counselor'), -- replace $realhash with hash generated during setup (see README)
  (2, 'counselor2@mentassist.com', '$realhash', 'counselor')
ON CONFLICT DO NOTHING;

INSERT INTO clients (id, counselor_id, first_name, last_name, dob) VALUES
  (1, 2, 'Maya',   'Johnson', '1990-03-14'),
  (2, 2, 'Daniel', 'Reyes',   '1985-11-22'),
  (3, 2, 'Priya',  'Nair',    '1998-07-09')
ON CONFLICT DO NOTHING;