from common import Config
from db.connection import get_db_connection
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse

logged_in_router = APIRouter()

debug = Config.debug
templates = Config.templates


@logged_in_router.get("/dashboard")
def dashboard():
    raise NotImplementedError


@logged_in_router.get("/welcome")
def welcome():
    raise NotImplementedError
