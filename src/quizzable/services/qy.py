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


class InvalidQuizFile(Exception):
    """
    The InvalidQuizFile exception is raised when the file content is not a valid quiz document.
    """


def parse_document(data) -> tuple[str | None, str, list]:
    """Split a loaded YAML document into ``(title, tags, questions)``.

    Two layouts are supported:

    - a bare list of question objects (no title, no tags)
    - a mapping with an optional ``title``, optional ``tags`` list, and a
      required ``questions`` list

    ``title`` is ``None`` when it is absent or blank, letting the caller decide
    on a fallback.
    """
    if isinstance(data, dict):
        title = data.get("title")
        tags = data.get("tags") or []
        questions = data.get("questions")
    else:
        title, tags, questions = None, [], data

    if not isinstance(questions, list) or not questions:
        raise InvalidQuizFile("The file must contain at least one question")

    # A blank or missing title becomes None so the caller can fall back
    title = (str(title).strip() if title else "") or None

    # Tags may be given as a list or a single string; store them newline-separated
    if isinstance(tags, str):
        tags = [tags]
    tags = "\n".join(stripped for tag in tags if (stripped := str(tag).strip()))

    return title, tags, questions


async def create_quiz_from_yaml(user: User, file: ui.upload.FileUpload):
    if not (mo := re.fullmatch(r"(.+)\.ya?ml", file.name)):
        raise InvalidFileName("Only .yaml or .yml files are supported")

    data = yaml.safe_load(await file.text())
    title, tags, questions = parse_document(data)

    # Fall back to the file name only when no title is set inside the file, and
    # enforce the strict naming rule just for that case.
    if title is None:
        name = mo.group(1)
        if not re.fullmatch(r"[-a-z0-9]+", name):
            raise InvalidFileName(
                "Name the file with lowercase letters, numbers and hyphens, "
                "or set a title inside the file"
            )
        title = totitle(name)

    try:
        quiz = await MCQuiz.create(title=title, tags=tags, maintainer=user)

    except IntegrityError as error:
        if re.search("UNIQUE.*quizzes.title", error.args[0].args[0]):
            raise DuplicateFileName()
        else:
            raise

    for index, questiondict in enumerate(questions, start=1):
        try:
            await MCQuestion.from_dict(validate(questiondict), quiz=quiz)
        except AssertionError as error:
            error.args.append(index)
            raise


def validate(questiondict: dict[str, str]) -> dict[str, str]:
    assert questiondict["q"], "Question text is missing"
    assert questiondict["a"], "Option A is missing"
    assert questiondict["b"], "Option B is missing"
    assert questiondict["c"], "Option C is missing"
    assert questiondict["d"], "Option D is missing"
    # Option 'e' is optional

    assert questiondict["k"], "There must be a correct choice"
    return questiondict
