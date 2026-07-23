from typing import Callable

from nicegui import app, ui

from ..models import User
from ..services import auth
from ..utils import is_authenticated


def card_template(
    action: str,
    primary: str,
    secondary: str,
    handler: Callable[[str, str], tuple[User, str]],
    toggle: Callable,
    redirect_url: str = "/home",
) -> ui.card:
    async def signup_or_login():
        try:
            user, token = await handler(username.value, password.value)
        except ValueError as error:
            ui.notify(error.args[0], color="negative")
        else:
            app.storage.user.update(auth=True, token=token, username=user.username)
            app.storage.client["user"] = user
            ui.navigate.to(redirect_url)

    with (
        ui.card()
        .classes("container max-w-md md:px-8 justify-center items-stretch aspect-4/3")
        .props(f'tag=form method=post action="{action}?{redirect_url=}"') as card
    ):
        ui.space()
        ui.label(primary).classes("text-2xl text-bold text-center")
        username = (
            ui.input("Username")
            .props("autofocus name=username")
            .on("keydown.enter", lambda: password.run_method("focus"))
        )
        password = (
            ui.input("Password", password=True, password_toggle_button=True)
            .props("name=password")
            .on("keydown.enter", lambda: btn.run_method("click"))
        )
        ui.input(value=redirect_url).props("name=redirect class=hidden")
        ui.space()

        with ui.card_actions().classes("text-xl"):
            btn = (
                ui.button(primary, on_click=signup_or_login)
                .props("no-caps rounded")
                .classes("text-lg text-bold px-4 md:px-8")
            )
            ui.space()
            ui.button(secondary, on_click=toggle).props("flat no-caps")

        ui.space()

    return card


def login_page(animate: bool = False, redirect_url: str = "/home"):
    if is_authenticated():
        return ui.navigate.to(redirect_url)

    # simple flip card animation using tailwind classes
    if animate:
        one = "z-1 rotate-y-0"
        two = "rotate-y-180"
        both = "absolute-center transition-transform duration-1000 -translate-1/2"
    else:
        one = ""
        two = "hidden"
        both = "absolute-center"

    def flip():
        for card in (login_card, signup_card):
            card.classes(toggle=f"{one} {two}")

    login_card = card_template(
        "auth/token",
        "Log in",
        "Sign up",
        redirect_url=redirect_url,
        handler=auth.login,
        toggle=flip,
    )
    signup_card = card_template(
        "auth",
        "Sign up",
        "Log in",
        redirect_url=redirect_url,
        handler=auth.signup,
        toggle=flip,
    )

    login_card.classes(f"{one} {both}")
    signup_card.classes(f"{two} {both}")
