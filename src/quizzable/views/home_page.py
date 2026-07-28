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

        # Dialog
        with (
            ui.dialog() as dialog,
            ui.card().classes("container max-w-lg text-primary"),
        ):
            with ui.row(wrap=False).classes("w-full justify-between items-center"):
                ui.label(quiz.title).classes("text-2xl mx-auto")
                with (
                    ui.button(icon="more_vert")
                    .classes("px-1")
                    .props("flat round")
                    .tooltip("more options"),
                    ui.menu().classes("text-primary"),
                ):
                    if owner:
                        ui.menu_item(
                            "Edit",
                            on_click=navigator(f"/quiz/{quiz.id}/edit"),
                        )
                        ui.menu_item(
                            "Delete",
                            on_click=lambda: background_tasks.create(delete(quiz)),
                        ).classes("text-negative")
                    ui.separator()
                    ui.menu_item("Share")

            ui.button("Attempt", on_click=navigator(f"/quiz/{quiz.id}")).props(
                "flat"
            ).classes("mx-auto")

        # Details
        ui.label(f"Number of questions: {count}")
        ui.label(maintainer_label)
        ui.button("Open", on_click=dialog.open).props("flat").classes("self-end")

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
