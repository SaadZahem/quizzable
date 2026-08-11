from nicegui import app, ui

from ..models import MCQuiz
from ..utils import protected
from ..widgets import error_card
from . import _quiz_editor


@protected
async def edit_quiz_page(quiz_id: int):
    user = app.storage.client["user"]
    quiz = await MCQuiz.filter(id=quiz_id).first()

    # more protection
    if user.id != quiz.maintainer_id:
        error_card(403, ["Forbidden"])
        return

    async with _quiz_editor.create(user, quiz):
        ui.label("Edit Quiz").classes("text-2xl text-bold")
