from nicegui import app, ui

from ..utils import navigator, protected
from ..widgets.question_card import QuestionCardContainer


@protected
async def new_quiz_page():
    with ui.column().classes(
        "grow self-stretch items-stretch 2xl:w-2xl 2xl:self-center"
    ):
        user = app.storage.client["user"]

        with ui.card().classes("items-center w-full max-w-md self-center") as main_card:
            ui.label("Create a new quiz").classes("text-2xl text-bold")
            title_input = ui.input(prefix="Title:").props(
                "autofocus dense outlined counter maxlength=255 autogrow"
            )

        container = QuestionCardContainer(user, title_input)
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
                .on("click", container.create_quiz)
                .props("outline no-caps")
                .classes("px-2 grow-1")
                .tooltip("finish")
            )
