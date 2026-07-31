import re

import yaml
from nicegui import ui
from tortoise.exceptions import IntegrityError

from ..models import MCQuestion, MCQuiz, User
from ..utils import totitle


class InvalidFileName(Exception):
    """
    The InvalidFileName exception is raised when the file name contains unsupported characters.
    """


class DuplicateFileName(Exception):
    """
    The DuplicateFileName exception is raised when the file name is duplicate or not unique.
    """


async def create_quiz_from_yaml(user: User, file: ui.upload.FileUpload):
    if not (mo := re.match(r"([-a-z0-9]+)\.ya?ml", file.name)):
        raise InvalidFileName()

    title = totitle(mo.group(1))
    data = yaml.safe_load(await file.text())

    try:
        quiz = await MCQuiz.create(title=title, maintainer=user)

    except IntegrityError as error:
        if re.search("UNIQUE.*quizzes.title", error.args[0].args[0]):
            raise DuplicateFileName()
        else:
            raise

    for index, questiondict in enumerate(data, start=1):
        try:
            await MCQuestion.from_dict(validate(questiondict), quiz=quiz)
        except AssertionError as error:
            error.args.append(index)
            raise


def validate(questiondict: dict[str, str]) -> dict[str, str]:
    assert questiondict["q"], "A question is missing"
    assert questiondict["a"], "Option A is missing"
    assert questiondict["b"], "Option B is missing"
    assert questiondict["c"], "Option C is missing"
    assert questiondict["d"], "Option D is missing"
    # Option 'e' is optional

    assert questiondict["k"], "There must be a correct choice"
    return questiondict
