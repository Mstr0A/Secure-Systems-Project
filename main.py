import os
import bcrypt
from dotenv import load_dotenv
from db.connection import get_db_connection
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, Response
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

load_dotenv()

app = FastAPI()

# Load the secret key
secret_key = os.getenv("SECRET_KEY")

# Validation
if secret_key is None:
    raise ValueError("Missing Secret Key for session middleware")

app.add_middleware(SessionMiddleware, secret_key=secret_key)

# Setup templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, name="root")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse, name="login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse, name="login_post")
async def login_post(
    request: Request, username: str = Form(...), password: str = Form(...)
):
    # Check if user is already logged in
    if request.session.get("username"):
        return templates.TemplateResponse(
            "logged.html",
            {"request": request, "username": request.session.get("username")},
        )

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT `password_hash` FROM `users` WHERE `username` = %s"
        values = (username,)

        cursor.execute(query, values)
        result = cursor.fetchone()

        if not result:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": "Username or password incorrect"},
            )

        match = bcrypt.checkpw(password.encode(), result["password_hash"].encode())

        if not match:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": "Username or password incorrect"},
            )

        # Set the session
        request.session["username"] = username

        return templates.TemplateResponse(
            "logged.html", {"request": request, "username": username}
        )

    except Exception as e:
        return Response(
            content=f"<h1>ERROR</h1><pre>{str(e)}</pre>",
            status_code=500,
            media_type="text/html",
        )

    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass


@app.get("/signup", response_class=HTMLResponse, name="signup")
async def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse, name="signup_post")
async def signup_post(
    request: Request, username: str = Form(...), password: str = Form(...)
):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT `password_hash` FROM `users` WHERE `username` = %s"
        values = (username,)

        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": "A user with that name already exists"},
            )

        # Generate the password hash
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        values = (username, password_hash)
        cursor.execute(query, values)
        connection.commit()

        return templates.TemplateResponse("signed.html", {"request": request})

    except Exception as e:
        return Response(
            content=f"<h1>ERROR</h1><pre>{str(e)}</pre>",
            status_code=500,
            media_type="text/html",
        )

    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass


@app.get("/logout", name="logout")
async def logout(request: Request):
    # Clear the session
    if request.session.get("username"):
        request.session.pop("username", None)

    return RedirectResponse(url="/", status_code=302)


if __name__ == "__main__":
    import uvicorn

    debug = os.getenv("DEBUG", "False").lower() == "true"

    if debug:
        uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=5050, workers=4)
