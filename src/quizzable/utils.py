from collections.abc import Callable
from pathlib import Path
from string import Template
from typing import Any

from nicegui import app, html, ui

from .models import User
from .services import auth

# nicegui.html is provides h1 but misses h2..6
for tag in (f"h{n}" for n in range(2, 7)):
    if not hasattr(html, tag):
        setattr(html, tag, html._create_html_element(tag))


def navigator(location, *, redirect: bool = False):
    def callback():
        nonlocal location

        if redirect and isinstance(location, str):
            url = app.storage.client.get("path").partition("?")[0]
            if location.partition("?")[0] != url:
                location += "&" if "?" in location else "?"
                location += "redirect_url="
                location += url

        ui.navigate.to(location)

    return callback


def totitle(name: str):
    return name.replace(*"- ").title()


def substitute(file: Path, context: dict):
    with file.open("rt") as f:
        content = f.read()

    template = Template(content)
    styles = template.safe_substitute(context)
    return styles


def logout():
    app.storage.user.update(auth=False, token="", username="")
    del app.storage.client["user"]
    if app.storage.client.get("protected"):
        ui.navigate.to("/")
    else:
        ui.navigate.reload()


def _auth() -> tuple[bool, dict[str, Any]]:
    if not app.storage.user.setdefault("auth", False):
        return False, {}

    token = app.storage.user["token"]
    verified, data = auth.verify_access_token(token)

    if not verified:
        app.storage.user.update(auth=False, username="")
        ui.notify("Session expired")
        if "user" in app.storage.client:
            del app.storage.client["user"]

    return verified, data


def is_authenticated() -> bool:
    return _auth()[0]


async def current_user() -> User | None:
    verified, data = _auth()
    if verified:
        username = data.get("sub")
        app.storage.user.update(username=username)
        return await auth.get_user(username)


def protected(func: Callable) -> Callable:
    """Decorator to mark a route handler as requiring authentication for the custom_sub_pages."""
    func._is_protected = True  # pylint: disable=protected-access
    return func


def is_protected(handler: Callable) -> bool:
    return getattr(handler, "_is_protected", False)
