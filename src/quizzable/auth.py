import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from nicegui import APIRouter, ui
from pwdlib import PasswordHash
from pydantic import BaseModel

from .models import User

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

password_hash = PasswordHash.recommended()
verify_password = password_hash.verify
get_password_hash = password_hash.hash

form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
token_dependency = Annotated[str, Depends(oauth2_scheme)]


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(username: str) -> User:
    return await User.filter(username=username).first()


async def authenticate_user(username: str, password: str) -> User | None:
    user = await get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user


@router.post("/token")
async def login_for_access_token(form: form_dependency) -> Token:
    user = await authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.page("/login")
def login_page(redir: str = "/"):
    with ui.element("form").props('action="token" method=post') as form:
        (
            ui.input("Username")
            .props("autofocus name=username")
            .on("keydown.enter", lambda: password.run_method("focus"))
        )
        password = (
            ui.input("Password", password=True, password_toggle_button=True)
            .props("name=password")
            .on("keydown.enter", lambda: form.run_method("submit"))
        )
        ui.button("Log in").props("type=submit")
        ui.link("Create a new account", "/auth")


@router.page("/")
def new_user_page():
    with ui.element("form").props("method=post"):
        ui.input("Username").props("autofocus name=username").on(
            "keydown.enter", lambda: password.run_method("focus")
        )
        password = ui.input(
            "Password", password=True, password_toggle_button=True
        ).props("name=password")
        ui.button("Create user").props("type=submit")
        ui.link("Login", "/auth/login")


@router.post("/")
async def create_new_user(form: form_dependency):
    await User.create(
        username=form.username,
        hashed_password=get_password_hash(form.password),
    )


async def get_current_user(token: token_dependency) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception

    username = payload.get("sub")
    user_id = payload.get("id")
    if username is None or user_id is None:
        raise credentials_exception

    user = get_user(username=username)
    if user is None or user.id != user_id:
        raise credentials_exception

    return user


user_dependency = Annotated[User, Depends(get_current_user)]


@router.get("/me")
def whoami(user: user_dependency):
    return repr(user)
