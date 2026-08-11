import os
from pathlib import Path

from dotenv import load_dotenv
from nicegui import app, ui
from tortoise.contrib.fastapi import register_tortoise

from .utils import substitute

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

# Theme configuration
COLORS = dict(
    primary="#6B705C",
    secondary="#DDBEA9",
    accent="#CB997E",
    myblack="#1A1A18",
    mywhite="#FAF8F5",
    brand="hsl(39, 77%, 90%)",
)
app.colors(**COLORS)

# Static files
templates_dir = Path(__file__).parent / "templates"

app.add_static_files("/yaml", "static/yaml")
# app.add_static_file(
# url_path="/static/fuse.js@7.0.0",
# local_file=templates_dir / "fuse.js",
# )

# Head html
ui.add_head_html(
    substitute(templates_dir / "header.html", COLORS),
    shared=True,
)

# Database configuration
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"quizzable": ["quizzable.models"]},
    generate_schemas=True,
)
