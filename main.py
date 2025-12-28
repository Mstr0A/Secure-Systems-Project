from fastapi import FastAPI
from dotenv import load_dotenv

# Load env before everything
load_dotenv()

from routes.root import root_router  # noqa: E402
from routes.auth import auth_router  # noqa: E402
from routes.logged_in import logged_in_router  # noqa: E402
from common import Config, SessionTimeoutMiddleware  # noqa: E402
from starlette.middleware.sessions import SessionMiddleware  # noqa: E402


app = FastAPI()
app.include_router(root_router)
app.include_router(auth_router)
app.include_router(logged_in_router)


# Validation
if Config.session_secret_key is None:
    raise ValueError("Missing Secret Key for session middleware")

app.add_middleware(SessionTimeoutMiddleware)
app.add_middleware(SessionMiddleware, secret_key=Config.session_secret_key)


if __name__ == "__main__":
    import uvicorn

    if Config.debug:
        uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=5050, workers=4)
