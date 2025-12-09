# 🤫 Whisper

Simple FastAPI authentication system with login and signup.

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

2. Create `.env` file with your database info and secret key:

```env
USER=your_db_user
PASSWORD=your_db_password
HOST=localhost
DATABASE=whisper
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Generate a secure secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
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

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5050
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
- Session management with encrypted cookies
- Simple dashboard
- Built with FastAPI for high performance

## Production

Set `DEBUG=False` in your `.env` file for production deployment.
