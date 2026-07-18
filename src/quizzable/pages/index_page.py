import random

from nicegui import html, ui

from ..utils import navigator
from ..widgets import header_element


@ui.page("/")
def index_page():
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
        (
            ui.button("Get started", on_click=navigator("/home"))
            .props("icon-right=arrow_forward no-caps rounded")
            .classes("text-lg text-bold")
        )

    # I don't know what to make out of this yet
    with container, ui.card().classes("hidden md:w-64 h-1/2 self-end"):
        ui.skeleton(animation="wave").classes("w-full")
        ui.card_section()
