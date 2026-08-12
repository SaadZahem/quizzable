from nicegui import app, events, ui

from ..services import qy
from ..utils import protected

INSTRUCTIONS = """
**Upload one or more YAML files — each file becomes a quiz.**

1. Name each file so it ends in `.yaml` or `.yml`.
2. Set the quiz title with a `title:` field. Without it, the title is taken from the file name, which must then use only lowercase letters, numbers and hyphens (`my-quiz.yml` becomes "My Quiz").
3. Optionally add `tags:` as a list.
4. List the questions under a `questions:` field. If you don't need a title or tags, the file can simply be the list of questions on its own.

<br>

Each question supports these keys:

| Key | Value | Optional |
|:---:|:------|:--------:|
|**q**| Question text | no |
|**a**| First choice | no |
|**b**| Second choice | no |
|**c**| Third choice | no |
|**d**| Fourth choice | no |
|**e**| Fifth choice | yes |
|**k**| Correct choice letter | no |

<hr><br>

**Example**
"""

EXAMPLE = """\
title: Cardiology Basics
tags:
  - cardiology
  - week 3
questions:
  - q: "What is the normal resting heart rate?"
    a: "40-60 bpm"
    b: "60-100 bpm"
    c: "100-120 bpm"
    d: "120-140 bpm"
    k: b"""


@protected
def upload_quiz_page():
    user = app.storage.client["user"]

    async def on_upload(e: events.UploadEventArguments):
        try:
            await qy.create_quiz_from_yaml(user, e.file)
        except AssertionError as error:
            message = "Object no. {1}: {0}".format(*error.args)
            ui.notify(message, color="negative")
        except qy.InvalidFileName as error:
            ui.notify(
                error.args[0] if error.args else "Invalid filename", color="negative"
            )
        except qy.InvalidQuizFile as error:
            ui.notify(error.args[0], color="negative")
        except qy.DuplicateFileName:
            ui.notify(
                "A quiz with this name already exists. Try changing the file name",
                color="negative",
            )

    (
        ui.upload(label="Upload yaml files", on_upload=on_upload)
        .classes("self-center")
        .props("accept='application/yaml, application/yml'")
    )

    with ui.card().classes("w-full min-w-0"):
        ui.markdown(INSTRUCTIONS).classes("text-base w-full")
        ui.codemirror(EXAMPLE, language="yaml").set_enabled(False)
