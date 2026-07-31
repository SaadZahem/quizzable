from nicegui import app, ui
from nicegui.events import UploadEventArguments

from ..services import qy
from ..utils import protected

INSTRUCTIONS = """
**Select yaml files to upload.** Each yaml file you upload will create a quiz.

1. The uploaded file name should only consist of lowercase characters "a-z" and numbers and only "-" as special character
2. The uploaded file name should end in either `.yaml` or `.yml`
3. The quiz title will be set to the file name. "quiz-title.yml" becomes "Quiz Title"
4. The file contains a list of objects, each represents an MCQ question. The supported keys are in the following table
5. Upload multiple files to create multiple quizzes at once

<br>

| Key | Value   |    Optional |
|:---:| ---------------------:| --- |
|**q**| The question text     | no  |
|**a**| First choice text     | no  |
|**b**| Second choice text    | no  |
|**c**| Third choice text     | no  |
|**d**| Fourth choice text    | no  |
|**e**| Fifth choice text     |*yes*|
|**k**| Correct choice letter | no  |

"""


@protected
def upload_quiz_page():
    user = app.storage.client["user"]

    async def on_upload(e: UploadEventArguments):
        try:
            await qy.create_quiz_from_yaml(user, e.file)
        except AssertionError as error:
            message = "Object no. {1}: {0}".format(*error.args)
            ui.notify(message, color="negative")
        except qy.InvalidFileName:
            ui.notify("Invalid filename", color="negative")
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

    with ui.card():
        ui.markdown(INSTRUCTIONS).classes("text-lg")
