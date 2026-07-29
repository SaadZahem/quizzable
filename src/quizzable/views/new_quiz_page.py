from nicegui import app, ui

from ..utils import protected
from . import _quiz_editor


@protected
async def new_quiz_page():
    user = app.storage.client["user"]

    async with _quiz_editor.create(user):
        ui.label("Create a new quiz").classes("text-2xl text-bold")
