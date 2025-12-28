from os import getenv
from fastapi.templating import Jinja2Templates


# This file includes all the config that is needed cross-files
class Config:
    debug = getenv("DEBUG", "False").lower() == "true"
    templates = Jinja2Templates(directory="templates")
    session_secret_key = getenv("SECRET_KEY")
    session_timeout = int(getenv("SESSION_TIMEOUT", "1800"))
