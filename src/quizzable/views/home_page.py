from nicegui import app, ui

from ..models import MCQuiz
from ..utils import navigator
from ..widgets import quiz_dialog


async def home_page():
    """View the home page."""

    # Accessing all quizzes
    all_quizzes = await MCQuiz.all()

    # Accessing the current user
    user = app.storage.client.get("user")

    async def remove(quiz: MCQuiz) -> None:
        """Remove a quiz from the list and from the database."""
        all_quizzes.remove(quiz)
        await quiz.delete()
        quiz_list.refresh()

    @ui.refreshable
    async def quiz_list():
        with ui.list().props("separator").classes("w-full"):
            for quiz in reversed(all_quizzes):
                for term in search.value:
                    if term.lower() not in quiz.title.lower():
                        break
                else:
                    dialog = await quiz_dialog.create(user, quiz, remove=remove)
                    with ui.item(on_click=dialog.open):
                        with ui.item_section().classes("grow-0 me-4"):
                            ui.icon("quiz").on("click")
                        with ui.item_section():
                            ui.label(quiz.title)

    # Enables app.storage.tab
    await ui.context.client.connected()

    # Main card element with search bar, a button, and a refreshable list
    with ui.card().classes("grow self-stretch items-center"):
        with (
            ui.input_chips("Search quizzes", on_change=quiz_list.refresh)
            .classes("self-stretch")
            .bind_value(app.storage.tab, "search") as search,
            search.add_slot("after"),
        ):
            (
                ui.button(icon="add", color="accent")
                .props("flat")
                .on("click", navigator("/quiz"))
                .tooltip("add a quiz")
            )

        await quiz_list()
