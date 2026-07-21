from datetime import timedelta

from fastapi import HTTPException, Request, status
from nicegui import APIRouter, app
from starlette.middleware.base import BaseHTTPMiddleware

from .models import Token, User
from .services.auth import (
    authenticate_user,
    create_access_token,
    form_dependency,
    get_password_hash,
    user_dependency,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@app.add_middleware
class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return await call_next(request)


@router.post("/token")
async def login_for_access_token(form: form_dependency) -> Token:
    user = await authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=1)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id},
        expires=access_token_expires,
    )
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
