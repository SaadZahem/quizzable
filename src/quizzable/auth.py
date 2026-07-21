from fastapi import Request
from nicegui import APIRouter, app
from starlette.middleware.base import BaseHTTPMiddleware

from .models import Token, User
from .services.auth import form_dependency, get_password_hash, login, user_dependency

router = APIRouter(prefix="/auth", tags=["auth"])


@app.add_middleware
class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return await call_next(request)


@router.post("/token")
async def login_for_access_token(form: form_dependency) -> Token:
    _, access_token = await login(form.username, form.password)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/")
async def create_new_user(form: form_dependency):
    await User.create(
        username=form.username,
        hashed_password=get_password_hash(form.password),
    )


@router.get("/whoami")
def whoami(user: user_dependency):
    return repr(user)
