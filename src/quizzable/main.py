import operator as op
import os
import random
import re
from itertools import count

from models import MCQuestion, MCQuiz
from nicegui import ElementFilter, app, html, ui
from tortoise.contrib.fastapi import register_tortoise

for tag in (f"h{n}" for n in range(2, 7)):
    if not hasattr(html, tag):
        setattr(html, tag, html._create_html_element(tag))

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
)
quizzes = []


def _navigate(location):
    def callback():
        ui.navigate.to(location)

    return callback


def totitle(name: str):
    return name.replace(*"- ").title()


def question_card(number, question: MCQuestion, value: str = "-", *, review=False):
    q = question
    choices = [q.a, q.b, q.c, q.d]
    if q.e:
        choices.append(q.e)

    with ui.card().classes("self-stretch") as card:
        if not review:
            html.strong(f"{number}. " + question.text)
            ui.radio(
                {
                    index: f"{prefix}) {choice}"
                    for index, prefix, choice in zip(range(5), "abcde", choices)
                },
            )
            return card

        # Question card for reviewing
        with ui.row().classes("w-full justify-end"):
            with ui.column():
                question_text = "{}. {}".format(number, question.text)
                html.strong(question_text)
                for prefix, choice in zip("abcde", choices):
                    choice_text = "{}) {}".format(prefix, choice)
                    label = ui.label(choice_text).classes("py-1 px-2 rounded-lg")

                    if prefix == question.correct.value:
                        label.classes("bg-green-300 text-[blue]")
                    elif prefix == value:
                        label.classes("bg-red-300 text-[blue]")

            ui.space().classes("grow")
            with ui.row().classes("self-stretch"):
                ui.separator().props("vertical")
                grade_text = "%i/1" % (value == question.correct.value)
                ui.label(grade_text).classes("my-auto text-end")

    return card


@ui.page("/update")
def update_page(*, redirect=True):
    global quizzes

    quizzes = [
        file.removesuffix(".yml")
        for file in os.listdir("data")
        if file.endswith(".yml")
    ]

    if redirect:
        ui.navigate.to(home_page)


@ui.page("/quiz/{file:str}")
async def quiz_page(file):
    assert file in quizzes

    quiz = await MCQuiz.filter(title=totitle(file)).first()
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


@ui.page("/quiz/{file:str}/{selection:str}")
async def result_page(file, selection):
    assert file in quizzes
    assert re.match("[-a-e]+", selection)

    quiz = await MCQuiz.filter(title=totitle(file)).first()
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
                    on_click=_navigate("/home"),
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
                    on_click=_navigate(f"/quiz/{file}"),
                ).bind_visibility_from(separator, "visible")


def header_element():
    with (
        html.header().classes("w-full py-4 shadow-inner-lg") as header,
        ui.row().classes("container mx-auto items-center"),
    ):
        with html.a().props('href="/"') as anchor, ui.element("h5"):
            anchor.classes("hover:underline")
            html.strong("Quizzable")

        ui.space()
        ui.link("update", "/update")

    return header.classes("border-b-1 border-dashed border-slate")


@ui.page("/home")
def home_page():

    @ui.refreshable
    def quiz_list():
        with ui.list().props("separator").classes("grow md:w-md"):
            for file in quizzes:
                for term in search.value:
                    if term not in file:
                        break
                else:
                    with ui.item():
                        ui.link(file.replace(*"- ").title(), f"quiz/{file}")

    ui.context.client.content.classes("p-0 gap-0 h-[100vh]")
    header_element().classes("bg-[wheat]")

    with (
        ui.element().classes("size-full py-8 bg-[wheat]"),
        ui.row().classes("h-full container mx-auto"),
        ui.card().classes("self-stretch grow justify-center items-center"),
    ):
        search = ui.input_chips("Search quizzes", on_change=quiz_list.refresh).classes(
            "self-stretch"
        )
        quiz_list()


@ui.page("/")
def landing_page():
    ui.context.client.content.classes("p-0 gap-0 h-[100vh]")
    header_element().classes("bg-[wheat]")

    with (
        ui.element().classes("size-full py-8 bg-[wheat]"),
        ui.row().classes("h-full container mx-auto") as container,
        ui.card().classes("self-stretch grow justify-center items-center"),
    ):
        hook_template = "{} your quizzes {}"
        verb = random.choice(["Attempt", "Make", "Share"])
        adverb = random.choice(["anytime", "anywhere", "anyhow"])
        hook = hook_template.format(verb, adverb)

        ui.label("Welcome to").classes("text-4xl")
        html.strong("Quizzable").classes("text-6xl")
        ui.label(hook).classes("italic text-2xl")
        ui.button("Get started", on_click=_navigate("/home")).props(
            'icon-right="arrow_forward" no-caps rounded'
        ).classes("text-lg text-bold")

    # I don't know what to make out of this yet
    with container, ui.card().classes("hidden md:w-64 h-1/2 self-end"):
        ui.skeleton(animation="wave").classes("w-full")
        ui.card_section()


update_page(redirect=False)
ui.run()
