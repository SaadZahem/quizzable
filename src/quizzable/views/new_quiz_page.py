from nicegui import ui

from ..models import User
from ..utils import protected


@protected
async def new_quiz_page(user: User):
    with ui.card().classes("grow self-stretch items-center"):
        ui.label("Create a new quiz").classes("text-2xl text-bold")
