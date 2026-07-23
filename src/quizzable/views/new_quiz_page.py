from nicegui import ui

from ..models import User
from ..utils import navigator, protected
from ..widgets.question_card import EditableQuestionCard, QuestionCardContainer


@protected
async def new_quiz_page(user: User):
    with ui.column().classes(
        "grow self-stretch items-stretch 2xl:w-2xl 2xl:self-center"
    ):
        with ui.card().classes("items-center w-full max-w-md self-center") as main_card:
            ui.label("Create a new quiz").classes("text-2xl text-bold")
            ui.input(prefix="Title:").props(
                "autofocus dense outlined counter maxlength=255 autogrow"
            )

        container = QuestionCardContainer[EditableQuestionCard]()
        ui.separator()
        with ui.row().classes("items-center justify-center md:justify-evenly"):
            (
                ui.button(color="secondary", icon="arrow_upward")
                .on("click", navigator(main_card))
                .props("outline")
                .classes("px-2")
                .tooltip("back to top")
            )
            (
                ui.button(color="primary", icon="add")
                .on("click", container.add_editable_question_card)
                .props("outline no-caps")
                .classes("px-2 grow")
                .tooltip("add a question card")
            )
            (
                ui.button(color="accent", icon="done")
                .on("click", container.add_editable_question_card)
                .props("outline no-caps")
                .classes("px-2")
                .tooltip("finish")
            )
