from collections import namedtuple
from typing import Callable

import httpx
from fastapi import HTTPException
from nicegui import app, ui

from .. import auth


def card_template(
    action: str,
    primary: str,
    secondary: str,
    on_click: Callable,
    toggle: Callable,
    redirect_url: str = "/home",
) -> ui.card:
    async def click():
        await on_click(dict(username=username.value, password=password.value))

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
                ui.button(primary)
                .props("no-caps rounded")
                .classes("text-lg text-bold px-4 md:px-8")
                .on("click", click)
            )
            ui.space()
            ui.button(secondary, on_click=toggle).props("flat no-caps")

        ui.space()

    return card


def login_page(animate: bool = False, redirect_url: str = "/home"):
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

    async def login(data: dict):
        Form = namedtuple("Form", ["username", "password"])
        form = Form(**data)
        try:
            token = await auth.login_for_access_token(form)
        except HTTPException:
            raise ValueError("Invalid credentials")
        else:
            app.storage.user.update(auth=True, token=token.access_token)
            ui.navigate.to(redirect_url)

    async def signup(data: dict):
        response = httpx.post("auth", data=data)
        if response.status_code == 200:
            await login(data)
        else:
            raise ValueError("Username already exists")

    login_card = card_template(
        "auth/token",
        "Log in",
        "Sign up",
        redirect_url=redirect_url,
        on_click=login,
        toggle=flip,
    )
    signup_card = card_template(
        "auth",
        "Sign up",
        "Log in",
        redirect_url=redirect_url,
        on_click=signup,
        toggle=flip,
    )

    login_card.classes(f"{one} {both}")
    signup_card.classes(f"{two} {both}")
