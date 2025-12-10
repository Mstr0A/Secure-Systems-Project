from fastapi import FastAPI
from dotenv import load_dotenv
from routes.root import root_router
from routes.auth import auth_router
from common import Config, SessionTimeoutMiddleware
from starlette.middleware.sessions import SessionMiddleware


load_dotenv()

app = FastAPI()
app.include_router(root_router)
app.include_router(auth_router)


# Validation
if Config.session_secret_key is None:
    raise ValueError("Missing Secret Key for session middleware")

app.add_middleware(SessionMiddleware, secret_key=Config.session_secret_key)
app.add_middleware(SessionTimeoutMiddleware)


if __name__ == "__main__":
    import uvicorn

    if Config.debug:
        uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=5050, workers=4)
