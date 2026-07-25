from nicegui import app, background_tasks, ui

from ..models import MCQuiz
from ..utils import navigator


async def home_page():
    all_quizzes = await MCQuiz.all()
    user = app.storage.client.get("user")

    async def delete(quiz: MCQuiz):
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
                    with ui.expansion(quiz.title, group="quiz").classes(
                        "w-full"
                    ) as expansion:
                        with expansion.add_slot("header"):
                            with ui.item_section().classes("grow-0 me-4"):
                                ui.icon("quiz").on("click")
                            with ui.item_section():
                                ui.label(quiz.title)
                        with expansion.add_slot("default"):
                            await quiz_details(quiz)

    async def quiz_details(quiz: MCQuiz):
        count = len(await quiz.questions)
        maintainer = (await quiz.maintainer).username
        owner = user and user.username == maintainer

        maintainer_label = f"Maintainer: {maintainer}"
        if owner:
            maintainer_label += " (You)"

        ui.label(f"Number of questions: {count}")
        ui.label(maintainer_label)
        with ui.row(align_items="center").classes("w-full gap-1"):
            ui.space()
            menu_button(quiz, owner)
            ui.button("Attempt", on_click=navigator(f"/quiz/{quiz.file}")).props("flat")

    def menu_button(quiz: MCQuiz, owner: bool):
        with (
            ui.button(icon="more_vert").classes("px-1").props("flat round"),
            ui.menu(),
        ):
            if owner:
                ui.menu_item("Edit")
                ui.menu_item(
                    "Delete", on_click=lambda: background_tasks.create(delete(quiz))
                )
            ui.separator()
            ui.menu_item("Share")

    await ui.context.client.connected()

    with ui.card().classes("grow self-stretch items-center"):
        with (
            ui.input_chips("Search quizzes", on_change=quiz_list.refresh)
            .classes("self-stretch")
            .bind_value(app.storage.tab, "search") as search,
            search.add_slot("after"),
        ):
            ui.button(icon="add", color="accent").props("flat").on(
                "click", navigator("/quiz")
            ).tooltip("add a quiz")

        await quiz_list()
