1. Run the following command with your docker containers built and running:
    - docker exec -i mentassistdb psql -U postgres_admin -d mentassist_app -c "SELECT email, length(password_hash), password_hash FROM users;"
    - This will show you what hash values are currently associated with the seed accounts.

2. If you need to update the hashes we will use the method outlined in the README:
    1. "import bcrypt; print(bcrypt.hashpw(b'password123', bcrypt.gensalt()).decode())" | Out-File -Encoding utf8 -FilePath hash.py
    2. docker run --rm -v "${PWD}:/scripts" python:3.12-alpine sh -c "pip install bcrypt -q && python3 /scripts/hash.py"
    3. Remove-Item hash.py
    4. Manually open seed_dev.sql and past the full hash in, save it, then rebuild:
        -> docker compose down -v
        -> docker compose up --build -d

3. I would recommend doing Step 1 again after the rebuild to see if the hashes updated. If they did NOT, then proceed with the following steps:
    - In PowerShell do the following:
    1. Save your generated hash as follows: 
        $hash = 'YOUR_HASH_HERE'
    2. With docker running, manually update the database:
        docker exec -i mentassistdb psql -U postgres_admin -d mentassist_app -c "UPDATE users SET password_hash = '$hash' WHERE email IN ('counselor1@mentassist.com', 'counselor2@mentassist.com');
    3. Verify: 
        docker exec -i mentassistdb psql -U postgres_admin -d mentassist_app -c "SELECT email, length(password_hash), password_hash FROM users;"