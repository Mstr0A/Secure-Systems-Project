from common import Config
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

templates = Config.templates

root_router = APIRouter()


@root_router.get("/", response_class=HTMLResponse, name="root")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
