import os

from models import load_questionset
from nicegui import ElementFilter, html, ui

quizzes = [file for file in os.listdir("data") if file.endswith(".yml")]


def question_card(number, question, value=None, *, reveal=False):
    with ui.card().classes("container") as card:
        html.strong(f"{number}. " + question.text)
        if reveal:
            for index, prefix, choice in zip(range(5), "abcde", question.choices):
                label = ui.label(f"{prefix}) {choice}")

                if index == question.correct:
                    label.classes("bg-green")
                elif index == value:
                    label.classes("bg-red")
        else:
            ui.radio(
                {
                    index: f"{prefix}) {choice}"
                    for index, prefix, choice in zip(
                        range(5), "abcde", question.choices
                    )
                },
                value=value,
            )
    return card.mark("question")


@ui.page("/update")
def update():
    global quizzes
    quizzes = [file for file in os.listdir("data") if file.endswith(".yml")]
    ui.navigate.to("/")


@ui.page("/quiz/{file:str}")
def quiz(file):
    assert file in quizzes
    questions = load_questionset(f"data/{file}")

    def submit():
        score, total = 0, 0
        radios = ElementFilter(kind=ui.radio)
        selection = ""

        for question, radio in zip(questions.values(), radios):
            total += 1
            score += int(radio.value == question.correct)
            selection += str(radio.value if radio.value is not None else "=")

        result = "####**%i/%i**\n(%.2f%%)" % (score, total, score / total * 100)

        with (
            ui.dialog(value=True),
            ui.card().classes("w-md"),
            ui.row().classes("w-full justify-center"),
        ):
            ui.markdown(result).classes("grow text-center my-auto text-lg")
            with ui.column().classes("items-stretch"):
                ui.button("Home", on_click=lambda: ui.navigate.to("/"))
                ui.button(
                    "Revise",
                    on_click=lambda: ui.navigate.to(f"/revise/{file}/{selection}"),
                )

    with ui.column().classes("w-full items-center gap-2"):
        for number, question in questions.items():
            question_card(number, question)

        ui.space()
        ui.button("Submit", on_click=submit)


@ui.page("/revise/{file:str}/{selection:str}")
def revise(file, selection):
    assert file in quizzes
    questions = load_questionset(f"data/{file}")

    with ui.column().classes("w-full items-center gap-2"):
        for (number, question), char in zip(questions.items(), selection):
            assert char in "=01234"
            value = None if char == "=" else int(char)
            question_card(number, question, value, reveal=True)

        ui.space()
        with ui.row():
            ui.button("Home", on_click=lambda: ui.navigate.to("/"))
            ui.button("Retry", on_click=lambda: ui.navigate.to(f"/quiz/{file}"))


@ui.page("/")
def home():
    with ui.row().classes("w-full"):
        html.strong("Quizzable")
        ui.link("update", "/update")
        ui.space()
        ui.label("Attempt your quizzes anytime")

    with ui.column():
        for file in quizzes:
            ui.link(file, f"quiz/{file}")


ui.run()
