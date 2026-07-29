from contextlib import asynccontextmanager

from nicegui import ui

from ..models import MCQuiz, User
from ..utils import navigator
from ..widgets import question_card_container


@asynccontextmanager
async def create(user: User, quiz: MCQuiz | None = None):
    if new_quiz := quiz is None:
        quiz = MCQuiz(maintainer=user)

    with (
        ui.column()
        .classes("grow self-stretch items-stretch")
        .classes("2xl:w-2xl 2xl:self-center")
    ):
        with ui.card().classes("items-center w-full max-w-md self-center") as main_card:
            # allows the caller to insert elements at the beginning and end of this card
            yield main_card

            title_input = (
                ui.input(prefix="Title:")
                .props("autofocus dense outlined counter maxlength=255 autogrow")
                .bind_value(quiz, "title")
            )

        container = question_card_container(user, quiz, title_input)
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
                .on("click", container.save)
                .props("outline no-caps")
                .classes("px-2 grow-1")
                .tooltip("save")
            )

    # Loading questions in case the quiz wasn't new
    if not new_quiz:
        async for question in quiz.questions:
            container.add_editable_question_card(question)
