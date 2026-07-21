from pathlib import Path
from string import Template

from nicegui import html, ui

# nicegui.html is provides h1 but misses h2..6
for tag in (f"h{n}" for n in range(2, 7)):
    if not hasattr(html, tag):
        setattr(html, tag, html._create_html_element(tag))


def navigator(location):
    def callback():
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
