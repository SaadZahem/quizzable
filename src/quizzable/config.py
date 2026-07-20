import os

from dotenv import load_dotenv
from nicegui import app
from tortoise.contrib.fastapi import register_tortoise

if not load_dotenv(".env"):
    raise ValueError(".env file is missing")


STORAGE_SECRET = os.getenv("STORAGE_SECRET")
"used to enable app.storage.user"

SECRET_KEY = os.getenv("SECRET_KEY")
"used to secure JWT tokens"

ALGORITHM = "HS256"
"widely used algorithm to secure JWT tokens"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
"the time after which a relogin is needed"

TOKEN_URL = "auth/token"
"the url from which the JWT token is obtained"


# Theme configuration
app.colors(
    primary="#6B705C",
    secondary="#DDBEA9",
    accent="#CB997E",
    black="#1A1A18",
    white="#FAF8F5",
)

# Database configuration
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["src.quizzable.models"]},
    generate_schemas=True,
)
