from nicegui import app, ui

from ..models import MCQuiz
from ..utils import protected
from . import _quiz_editor


@protected
async def edit_quiz_page(quiz_id: int):
    user = app.storage.client["user"]
    quiz = await MCQuiz.filter(id=quiz_id).first()

    async with _quiz_editor.create(user, quiz):
        ui.label("Edit quiz").classes("text-2xl text-bold")
