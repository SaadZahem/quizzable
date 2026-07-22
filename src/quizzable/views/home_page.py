from nicegui import app, ui

from ..models import MCQuiz
from ..utils import navigator


async def home_page():
    await ui.context.client.connected()
    all_quizzes = await MCQuiz.all()

    @ui.refreshable
    async def quiz_list():
        with ui.list().props("separator").classes("w-full"):
            for quiz in all_quizzes:
                for term in search.value:
                    if term.lower() not in quiz.title.lower():
                        break
                else:
                    with ui.expansion(quiz.title, group="quiz").classes("w-full"):
                        await quiz_details(quiz)

    async def quiz_details(quiz: MCQuiz):
        if quiz:
            title = quiz.title
            count = len(await quiz.questions)
            maintainer = (await quiz.maintainer).username

            ui.label(title).classes("text-3xl")
            ui.label(f"Number of questions: {count}")
            ui.label(f"Maintainer: {maintainer}")
            (
                ui.button("Attempt", on_click=navigator(f"/quiz/{quiz.file}"))
                .props("flat")
                .classes("self-end")
            )
        else:
            ui.label("None is selected").classes("mx-auto")

    with ui.card().classes("grow self-stretch items-center"):
        with (
            ui.input_chips("Search quizzes", on_change=quiz_list.refresh)
            .classes("self-stretch")
            .bind_value(app.storage.tab, "search") as search
        ):
            with search.add_slot("after"):
                ui.button(icon="add", color="accent").props("flat").on(
                    "click", navigator("quiz")
                ).tooltip("add a quiz")

        await quiz_list()
