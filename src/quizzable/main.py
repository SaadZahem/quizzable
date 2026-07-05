import os

from models import load_questionset
from nicegui import html, ui

quizzes = [file for file in os.listdir("data") if file.endswith(".yml")]


@ui.page("/update")
def update():
    global quizzes
    quizzes = [file for file in os.listdir("data") if file.endswith(".yml")]
    ui.navigate.to("/")


@ui.page("/quiz/{file:str}")
def quiz(file):
    assert file in quizzes
    questions = load_questionset(f"data/{file}")
    radios = []

    def submit():
        score, total = 0, 0
        for question, radio in zip(questions.values(), radios):
            total += 1
            score += int(radio.value == question.correct)

        ui.notify(f"{score}/{total}")

    with ui.column().classes("w-full items-center gap-2"):
        for number, question in questions.items():
            with ui.card().classes("container"):
                html.strong(f"{number}. " + question.text)
                radio = ui.radio(
                    {
                        index: f"{prefix}) {choice}"
                        for index, (prefix, choice) in enumerate(
                            zip("abcde", question.choices)
                        )
                    }
                )
                radios.append(radio)

        ui.button("Submit", on_click=submit)


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
