from nicegui import app, ui

from ..models import MCQuiz
from ..utils import navigator, totitle


async def home_page():
    storage_file: str = app.storage.tab.get("file", "")
    all_quizzes = await MCQuiz.all()

    async def select(file):
        app.storage.tab.update(file=file)
        quiz_details.refresh(file)

    @ui.refreshable
    def quiz_list():
        with ui.list().props("separator"):
            for quiz in all_quizzes:
                for term in search.value:
                    if term.lower() not in quiz.title.lower():
                        break
                else:
                    ui.item(quiz.title, on_click=lambda q=quiz: select(q.file))

    @ui.refreshable
    async def quiz_details(file: str):
        quiz = (
            await MCQuiz.filter(title=totitle(file))
            .prefetch_related("questions")
            .first()
        )

        if quiz:
            title = quiz.title
            count = len(quiz.questions)

            ui.label(title).classes("text-3xl")
            ui.label(f"Number of questions: {count}")
            (
                ui.button("Attempt", on_click=navigator(f"/quiz/{file}"))
                .props("flat")
                .classes("self-end")
            )
        else:
            ui.label("None is selected").classes("mx-auto")

    with ui.card().classes("grow self-stretch justify-center items-center"):
        search = (
            ui.input_chips("Search quizzes", on_change=quiz_list.refresh)
            .classes("self-stretch")
            .bind_value(app.storage.tab, "search")
        )
        with ui.row().classes("grow self-stretch"):
            quiz_list()
            with ui.column().classes("self-stretch mx-auto"):
                await quiz_details(storage_file)
