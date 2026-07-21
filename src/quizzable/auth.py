from fastapi import Request
from nicegui import APIRouter, app
from starlette.middleware.base import BaseHTTPMiddleware

from .models import Token
from .services import auth

router = APIRouter(prefix="/auth", tags=["auth"])


@app.add_middleware
class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return await call_next(request)


@router.post("/token")
async def login_for_access_token(form: auth.form_dependency) -> Token:
    _, access_token = await auth.login(form.username, form.password)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/")
async def create_new_user(form: auth.form_dependency):
    await auth.create_new_user(form.username, form.password)


@router.get("/whoami")
def whoami(user: auth.user_dependency):
    return repr(user)
