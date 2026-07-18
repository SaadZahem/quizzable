import os

from dotenv import load_dotenv
from nicegui import app, ui
from tortoise.contrib.fastapi import register_tortoise

if not load_dotenv(".env"):
    raise ValueError(".env file is missing")

from . import auth, pages

__all__ = [
    "auth",
    "main",
    "pages",
    "STORAGE_SECRET",
]
STORAGE_SECRET = os.getenv("STORAGE_SECRET")


def main(**kwargs):
    register_tortoise(
        app,
        db_url="sqlite://db.sqlite3",
        modules={"models": ["src.quizzable.models"]},
        generate_schemas=True,
    )
    app.include_router(auth.router)
    ui.run(title="Quizzable", language="en-US", storage_secret=STORAGE_SECRET, **kwargs)


if __name__ in {"__main__", "__mp_main__"}:
    main()
