from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, TOKEN_URL
from ..models import User
from ..utils import dependency

password_hash = PasswordHash.recommended()
verify_password = password_hash.verify
get_password_hash = password_hash.hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
token_dependency = dependency(str, oauth2_scheme)
form_dependency = dependency(OAuth2PasswordRequestForm)


async def create_new_user(username: str, password: str) -> User:
    return await User.create(
        username=username,
        hashed_password=get_password_hash(password),
    )


def create_access_token(data: dict, expires: timedelta | None = None):
    if expires is None:
        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user(username: str) -> User:
    return await User.filter(username=username).first()


async def authenticate_user(username: str, password: str) -> User:
    user = await get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def login(username: str, password: str) -> tuple[User, str]:
    user = await authenticate_user(username.strip(), password)
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data=dict(sub=user.username, id=user.id),
        expires=access_token_expires,
    )
    return user, access_token


async def signup(username: str, password: str) -> tuple[User, str]:
    user = await create_new_user(username.strip(), password)
    access_token = create_access_token(data=dict(sub=user.username, id=user.id))
    return user, access_token


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
    expires = payload.get("exp")

    if datetime.fromtimestamp(expires, timezone.utc) <= datetime.now(timezone.utc):
        raise credentials_exception

    if username is None or user_id is None:
        raise credentials_exception

    user = await get_user(username=username)
    if user is None or user.id != user_id:
        raise credentials_exception

    return user


user_dependency = dependency(User, get_current_user)
