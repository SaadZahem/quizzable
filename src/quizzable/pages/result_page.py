import operator as op
import re
from itertools import count

from nicegui import ui

from ..models import MCQuiz
from ..utils import navigator, totitle
from ..widgets import question_card


@ui.page("/quiz/{file:str}/{selection:str}")
async def result_page(file, selection):
    assert re.match("[-a-e]+", selection)

    quiz = await MCQuiz.filter(title=totitle(file)).first()
    assert quiz is not None

    questions = await quiz.questions
    total = len(questions)
    score = sum(
        question.correct.value == choice
        for question, choice in zip(questions, selection)
        if choice != "="
    )
    result = "####**%i/%i**\n(%.2f%%)" % (score, total, score / total * 100)

    def review():
        with container:
            for number, question, char in zip(count(1), questions, selection):
                assert char in "-abcde"
                value = None if char == "-" else char
                question_card(number, question, value, review=True)

        separator.set_visibility(True)

    ui.context.client.content.classes("bg-[wheat] min-h-[100vh]")
    with ui.column().classes("container mx-auto"):
        container = ui.column().classes("self-stretch items-center gap-2")
        separator = ui.separator().set_visibility(False)

        with (
            ui.card().classes("w-full md:w-md self-center"),
            ui.row().classes("w-full"),
        ):
            ui.markdown(result).classes("grow text-center my-auto text-lg")
            with ui.column().classes("items-stretch"):
                ui.button(
                    "Return",
                    icon="home",
                    on_click=navigator("/home"),
                )
                ui.button(
                    "Review",
                    color="positive",
                    icon="check",
                    on_click=review,
                ).bind_visibility_from(separator, "visible", op.not_)
                ui.button(
                    "Retry",
                    color="negative",
                    icon="repeat",
                    on_click=navigator(f"/quiz/{file}"),
                ).bind_visibility_from(separator, "visible")
