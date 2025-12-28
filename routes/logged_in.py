from common import Config
from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

logged_in_router = APIRouter()

debug = Config.debug
templates = Config.templates


@logged_in_router.get("/dashboard", response_class=HTMLResponse, name="dashboard")
def dashboard(request: Request):
    try:
        # Check if user is already logged in
        if request.session.get("username"):
            return templates.TemplateResponse(
                "logged.html",
                {"request": request, "username": request.session.get("username")},
            )
        else:
            RedirectResponse("/login", status_code=303)
    except Exception as e:
        return Response(
            content=f"<h1>ERROR</h1><pre>{str(e)}</pre>" if debug else "",
            status_code=500,
            media_type="text/html",
        )
