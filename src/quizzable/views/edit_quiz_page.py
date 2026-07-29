from nicegui import app, ui

from ..models import MCQuiz
from ..utils import navigator, protected
from ..widgets import question_card_container


@protected
async def edit_quiz_page(quiz_id: int):
    quiz = await MCQuiz.filter(id=quiz_id).first()

    with ui.column().classes(
        "grow self-stretch items-stretch 2xl:w-2xl 2xl:self-center"
    ):
        user = app.storage.client["user"]

        with ui.card().classes("items-center w-full max-w-md self-center") as main_card:
            ui.label("Edit quiz").classes("text-2xl text-bold")
            title_input = (
                ui.input(prefix="Title:")
                .props("autofocus dense outlined counter maxlength=255 autogrow")
                .bind_value(quiz, "title")
            )

        container = question_card_container(user, title_input, quiz)
        ui.separator()
        with ui.row().classes("items-center justify-center md:justify-evenly"):
            (
                ui.button(color="secondary", icon="arrow_upward")
                .on("click", navigator(main_card))
                .props("outline")
                .classes("px-2 grow-1")
                .tooltip("back to top")
            )
            (
                ui.button(color="primary", icon="add")
                .on("click", container.add_editable_question_card)
                .props("outline no-caps")
                .classes("px-2 grow-4")
                .tooltip("add a question card")
            )
            (
                ui.button(color="accent", icon="done")
                .on("click", container.save_quiz)
                .props("outline no-caps")
                .classes("px-2 grow-1")
                .tooltip("save")
            )

    async for question in quiz.questions:
        container.add_editable_question_card(question)
