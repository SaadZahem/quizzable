from typing import Callable

from nicegui import ui

from ..widgets import header_element


def card_template(action: str, primary: str, secondary: str, on_click: Callable):
    with (
        ui.card()
        .classes("container max-w-md md:px-8 justify-center items-stretch aspect-4/3")
        .props(f"tag=form method=post action={action}") as card
    ):
        ui.space()
        ui.label(primary).classes("text-2xl text-bold text-center")
        (
            ui.input("Username")
            .props("autofocus name=username")
            .on("keydown.enter", lambda: password.run_method("focus"))
        )
        password = (
            ui.input("Password", password=True, password_toggle_button=True)
            .props("name=password")
            .on("keydown.enter", lambda: btn.run_method("click"))
        )
        ui.space()

        with ui.card_actions().classes("text-xl"):
            btn = (
                ui.button(primary)
                .props("type=submit no-caps rounded")
                .classes("text-lg text-bold px-4 md:px-8")
            )
            ui.space()
            ui.button(secondary, on_click=on_click).props("flat no-caps")

        ui.space()

    return card


@ui.page("/login")
def login_page(animate: bool = False):
    # simple flip card animation using tailwind classes
    if animate:
        one = "z-1 rotate-y-0"
        two = "rotate-y-180"
        both = (
            "w-full absolute-center transition-transform duration-1000 -translate-1/2"
        )
    else:
        one = ""
        two = "hidden"
        both = "absolute-center"

    def switch():
        for card in (login_card, signup_card):
            card.classes(toggle=f"{one} {two}")

    ui.query(".nicegui-content").classes("p-0 gap-0 h-[100vh]")
    header_element().classes("bg-[wheat]")

    with (
        ui.element().classes("size-full py-8 bg-[wheat]"),
        ui.element().classes("h-full container mx-auto relative"),
    ):
        login_card = card_template("auth/token", "Log in", "Sign up", on_click=switch)
        signup_card = card_template("auth", "Sign up", "Log in", on_click=switch)

        login_card.classes(f"{one} {both}")
        signup_card.classes(f"{two} {both}")
