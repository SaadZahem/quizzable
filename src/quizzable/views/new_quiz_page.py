from nicegui import app, ui

from ..utils import protected
from . import _quiz_editor


@protected
async def new_quiz_page():
    user = app.storage.client["user"]

    async with _quiz_editor.create(user) as card:
        ui.label("New Quiz").classes("text-2xl text-bold")

    # Inserting a link to the upload page at the end of the card
    with card, ui.element("span"):
        ui.link("Upload", "/quiz/upload")
        ui.label(" yaml files instead").classes("inline")
