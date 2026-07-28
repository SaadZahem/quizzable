from nicegui import ElementFilter, ui

from ..models import MCQuiz
from ..widgets import error_card, question_card


async def load_quiz_page(quiz_id: str):
    quiz = await MCQuiz.filter(id=int(quiz_id)).first()
    if quiz is None:
        error_card(
            [
                "Quiz not found",
                f"We couldn't find the quiz with the id {quiz_id!r}",
                "Recheck the url and retry again",
            ]
        )
        return

    questions = await quiz.questions

    def submit():
        selection = ""

        for radio in ElementFilter(kind=ui.radio):
            selection += "abcde"[radio.value] if radio.value is not None else "-"

        ui.navigate.to(f"/quiz/{quiz_id}/review/{selection}")

    for number, question in enumerate(questions, start=1):
        question_card(number, question)

    ui.separator()
    ui.button("Submit", on_click=submit).classes("px-8 self-center")
    ui.space().classes("h-32")
