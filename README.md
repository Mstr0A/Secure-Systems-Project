# 🤫 Whisper

Simple Flask authentication system with login and signup.

(Made by Ameen)

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

   Or with pip:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file with your database info:
   ```env
   USER=your_db_user
   PASSWORD=your_db_password
   HOST=localhost
   DATABASE=whisper
   ```

3. Create a database with the following SQL:
   ```sql
   CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
    );
   ```

## Run

```bash
uv run main.py
```

Or with python:

```bash
python main.py
```

Open `http://localhost:5050` in your browser.

### Docker

```bash
docker build -t whisper .
docker run -p 5050:5050 --env-file .env whisper
```

## Features

- User signup and login
- Bcrypt password hashing
- Session management
- Simple dashboard
