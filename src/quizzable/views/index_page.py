import random

from nicegui import html, ui

from ..utils import navigator


async def index_page():
    with ui.card().classes("self-stretch grow justify-center items-center"):
        hook_template = "{} your quizzes {}"
        verb = random.choice(["Attempt", "Make", "Share"])
        adverb = random.choice(["anytime", "anywhere", "anyhow"])
        hook = hook_template.format(verb, adverb)

        ui.label("Welcome to").classes("text-4xl")
        html.strong("Quizzable").classes("text-6xl")
        ui.label(hook).classes("italic text-2xl text-center")
        (
            ui.button("Get started", on_click=navigator("/home"))
            .props("icon-right=arrow_forward no-caps rounded")
            .classes("text-lg text-bold")
        )

    await ui.context.client.connected()

    # I don't know what to make out of this yet
    with ui.card().classes("hidden md:w-64 h-1/2 self-end"):
        ui.skeleton(animation="wave").classes("w-full")
        ui.card_section()
