from pathlib import Path
from string import Template
from typing import Annotated

from fastapi import Depends
from nicegui import app, html, ui

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


def dependency(kind, func=None):
    if func is not None:
        return Annotated[kind, Depends(func)]
    else:
        return Annotated[kind, Depends()]
