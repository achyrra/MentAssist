-- DEV ONLY SEED DATA
INSERT INTO users (id, email, password_hash, role, first_name, last_name) VALUES
  (1, 'counselor1@mentassist.com', '$2b$12$bsMYWQS45eQDKM0H1daHhOGuLN1i0uEBWzVTR0mUSifQAfEXFbsVa', 'counselor', 'Counselor', 'One'),
  (2, 'counselor2@mentassist.com', '$2b$12$DKj2g5Xh35gE/IKIfFJnLeG1olGh1XUkIky7FzamtwjN3FfbtFxtG', 'counselor', 'Counselor', 'Two')
ON CONFLICT DO NOTHING;

INSERT INTO clients (counselor_id, first_name, last_name, dob)
SELECT id, 'Maya', 'Johnson', '1990-03-14' FROM users WHERE email='counselor2@mentassist.com'
ON CONFLICT DO NOTHING;

INSERT INTO clients (counselor_id, first_name, last_name, dob)
SELECT id, 'Daniel', 'Reyes', '1985-11-22' FROM users WHERE email='counselor2@mentassist.com'
ON CONFLICT DO NOTHING;

INSERT INTO clients (counselor_id, first_name, last_name, dob)
SELECT id, 'Priya', 'Nair', '1998-07-09' FROM users WHERE email='counselor2@mentassist.com'
ON CONFLICT DO NOTHING;

-- Reset sequences so auto-generated IDs start after seeded data
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('clients_id_seq', (SELECT MAX(id) FROM clients));
