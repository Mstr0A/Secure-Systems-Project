import bcrypt
from common import Config
from db.connection import get_db_connection
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse

auth_router = APIRouter()

debug = Config.debug
templates = Config.templates


@auth_router.get("/login", response_class=HTMLResponse, name="login")
async def login_get(request: Request):
    # Check if user is already logged in
    if request.session.get("username"):
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login", name="login_post")
async def login_post(
    request: Request, username: str = Form(...), password: str = Form(...)
):
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

        return RedirectResponse("/dashboard", status_code=303)

    except Exception as e:
        return Response(
            content=f"<h1>ERROR</h1><pre>{str(e)}</pre>" if debug else "",
            status_code=500,
            media_type="text/html",
        )

    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass


@auth_router.get("/signup", response_class=HTMLResponse, name="signup")
async def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@auth_router.post("/signup", response_class=HTMLResponse, name="signup_post")
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
            content=f"<h1>ERROR</h1><pre>{str(e)}</pre>" if debug else "",
            status_code=500,
            media_type="text/html",
        )

    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass


@auth_router.get("/logout", name="logout")
async def logout(request: Request):
    # Clear the session
    if request.session.get("username"):
        request.session.pop("username", None)

    return RedirectResponse(url="/", status_code=302)
