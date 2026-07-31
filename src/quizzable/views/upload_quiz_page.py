from nicegui import ui
from nicegui.events import UploadEventArguments

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
    def on_upload(e: UploadEventArguments): ...

    with ui.card():
        ui.markdown(INSTRUCTIONS).classes("text-lg")

    (
        ui.upload(on_upload=on_upload)
        .classes("self-center")
        .props("accept='application/yaml, application/yml'")
    )
