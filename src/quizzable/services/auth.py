from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from tortoise.exceptions import IntegrityError

from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from ..models import User


def dep(kind, func=None):
    if func is not None:
        return Annotated[kind, Depends(func)]
    else:
        return Annotated[kind, Depends()]


password_hash = PasswordHash.recommended()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
# token_dependency = dep(str, oauth2_scheme)
# form_dependency = dep(OAuth2PasswordRequestForm)

# credentials_exception = HTTPException(
# status_code=status.HTTP_401_UNAUTHORIZED,
# detail="Could not validate credentials",
# headers={"WWW-Authenticate": "Bearer"},
# )


async def create_new_user(username: str, password: str) -> User:
    return await User.create(
        username=username,
        hashed_password=password_hash.hash(password),
    )


def create_access_token(
    data: dict[str, Any],
    expire_timedelta: timedelta | None = None,
) -> str:
    if expire_timedelta is None:
        expire_timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expire_timedelta
    payload = {**data, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> tuple[bool, dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload["exp"]
        data = payload

        del payload["exp"]
        del payload

    except InvalidTokenError:
        return False, {}
    except KeyError:
        return False, data

    # comparing timestamps (float)
    if exp_timestamp <= datetime.now(timezone.utc).timestamp():
        return False, data

    return True, data


async def get_user(username: str) -> User:
    return await User.filter(username=username).first()


async def authenticate_user(username: str, password: str) -> User:
    user = await get_user(username)
    if user and password_hash.verify(password, user.hashed_password):
        return user

    raise ValueError("Wrong username or password")


async def login(username: str, password: str) -> tuple[User, str]:
    user = await authenticate_user(username.strip(), password)
    access_token = create_access_token(data=dict(sub=user.username))
    return user, access_token


async def signup(username: str, password: str) -> tuple[User, str]:
    try:
        user = await create_new_user(username.strip(), password)
    except IntegrityError:
        raise ValueError("Username already exists")
    else:
        access_token = create_access_token(dict(sub=user.username, id=user.id))
        return user, access_token
