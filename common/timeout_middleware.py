import time
from .config import Config
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class SessionTimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if "username" in request.session:
            last_activity = request.session.get("last_activity")

            if last_activity and time.time() - last_activity > Config.session_timeout:
                request.session.clear()
                return RedirectResponse(url="/login", status_code=303)

            request.session["last_activity"] = time.time()

        return await call_next(request)
