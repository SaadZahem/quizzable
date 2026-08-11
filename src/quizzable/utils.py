from pathlib import Path
from string import Template
from typing import Any, Callable

from nicegui import app, html, ui

from .models import User
from .services import auth

# nicegui.html provides h1 but is missing h2..6
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


async def copy_relative_url(relative_path: str):
    origin = await ui.run_javascript("window.location.origin")
    full_url = "{}/{}".format(
        origin.rstrip("/"),
        relative_path.lstrip("/"),
    )
    ui.clipboard.write(full_url)
    ui.notify(f"Copied: {full_url}")


def totitle(name: str):
    return name.replace(*"- ").title()


def substitute(file: Path, context: dict[str, Any]) -> str:
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
        ui.notify("Session expired!")
        app.storage.user.update(auth=False, username="")
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
