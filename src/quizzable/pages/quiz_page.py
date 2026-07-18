from nicegui import ElementFilter, ui

from ..models import MCQuiz
from ..utils import totitle
from ..widgets import question_card


@ui.page("/quiz/{file:str}")
async def quiz_page(file):
    quiz = await MCQuiz.filter(title=totitle(file)).first()
    assert quiz is not None

    questions = await quiz.questions

    def submit():
        selection = ""

        for radio in ElementFilter(kind=ui.radio):
            selection += "abcde"[radio.value] if radio.value is not None else "-"

        ui.navigate.to(f"/quiz/{file}/{selection}")

    ui.context.client.content.classes("bg-[wheat] min-h-[100vh]")

    with ui.column().classes("h-full container mx-auto"):
        for number, question in enumerate(questions, start=1):
            question_card(number, question)

        ui.separator()
        ui.button("Submit", on_click=submit).classes("px-8 self-center")
        ui.space().classes("h-32")
