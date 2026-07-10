import operator as op
import os
import re

from models import load_questionset
from nicegui import ElementFilter, html, ui

quizzes = [file for file in os.listdir("data") if file.endswith(".yml")]


def question_card(number, question, value=None, *, reveal=False):
    with ui.card().classes("container") as card:
        if reveal:
            with ui.row().classes("w-full justify-end"):
                with ui.column():
                    question_text = "{}. {}".format(number, question.text)
                    html.strong(question_text)
                    for index, prefix, choice in zip(
                        range(5), "abcde", question.choices
                    ):
                        choice_text = "{}) {}".format(prefix, choice)
                        label = ui.label(choice_text).classes("py-1 px-2 rounded-lg")

                        if index == question.correct:
                            label.classes("bg-green-300 text-[blue]")
                        elif index == value:
                            label.classes("bg-red-300 text-[blue]")

                ui.space().classes("grow")
                ui.separator().props("vertical")
                grade_text = "%i/1" % (value == question.correct)
                ui.label(grade_text).classes("my-auto text-end")
        else:
            html.strong(f"{number}. " + question.text)
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
def update_page():
    global quizzes
    quizzes = [file for file in os.listdir("data") if file.endswith(".yml")]
    ui.navigate.to("/")


@ui.page("/quiz/{file:str}")
def quiz_page(file):
    assert file in quizzes

    questions = load_questionset(f"data/{file}")

    def submit():
        selection = ""

        for radio in ElementFilter(kind=ui.radio):
            selection += str(radio.value if radio.value is not None else "=")

        ui.navigate.to(f"/quiz/{file}/{selection}")

    with ui.column().classes("w-full items-center gap-2"):
        for number, question in questions.items():
            question_card(number, question)

        ui.separator()
        ui.button("Submit", on_click=submit)
        ui.space().classes("h-64")


@ui.page("/quiz/{file:str}/{selection:str}")
def result_page(file, selection):
    assert file in quizzes
    assert re.match("[=0-4]+", selection)

    questions = load_questionset(f"data/{file}")
    total = len(questions)
    score = sum(
        question.correct == int(choice)
        for question, choice in zip(questions.values(), selection)
        if choice != "="
    )
    result = "####**%i/%i**\n(%.2f%%)" % (score, total, score / total * 100)

    def review():
        with container:
            for (number, question), char in zip(questions.items(), selection):
                assert char in "=01234"
                value = None if char == "=" else int(char)
                question_card(number, question, value, reveal=True)

        action.set_visibility(False)

    container = ui.column().classes("w-full items-center gap-2")

    with (
        ui.card().classes("container md:w-md self-center"),
        ui.row().classes("w-full justify-center"),
    ):
        ui.markdown(result).classes("grow text-center my-auto text-lg")
        with ui.column().classes("items-stretch"):
            ui.button("Home", on_click=lambda: ui.navigate.to("/"))
            action = ui.button("Review").on("click", review)
            ui.button(
                "Retry", on_click=lambda: ui.navigate.to(f"/quiz/{file}")
            ).bind_visibility_from(action, "visible", op.not_)


@ui.page("/")
def home_page():
    with ui.row().classes("w-full"):
        html.strong("Quizzable")
        ui.link("update", "/update")
        ui.space()
        ui.label("Attempt your quizzes anytime")

    with ui.column():
        for file in quizzes:
            ui.link(file, f"quiz/{file}")


ui.run()
