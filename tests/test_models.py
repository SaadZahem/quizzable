import pytest

from quizzable.models import ChoiceEnum, MCQuestion, MCQuiz


@pytest.mark.parametrize("value", list("abcde"))
def test_choiceenum_forward_valid_letters(value):
    assert ChoiceEnum.forward(value) is ChoiceEnum(value)


def test_choiceenum_forward_none():
    assert ChoiceEnum.forward(None) is None


@pytest.mark.parametrize("value", ["", "z", "A", "1"])
def test_choiceenum_forward_invalid(value):
    assert ChoiceEnum.forward(value) is None


def test_mcquiz_file_name_from_title():
    assert MCQuiz(title="My Cool Quiz").file == "my-cool-quiz.yml"


def test_mcquestion_as_dict_without_optional_choice():
    question = MCQuestion(
        text="Q?", a="1", b="2", c="3", d="4", e=None, correct=ChoiceEnum.c
    )
    assert question.as_dict() == {
        "q": "Q?",
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "k": "c",
    }


def test_mcquestion_as_dict_includes_optional_choice():
    question = MCQuestion(
        text="Q?", a="1", b="2", c="3", d="4", e="5", correct=ChoiceEnum.e
    )
    assert question.as_dict()["e"] == "5"
    assert question.as_dict()["k"] == "e"
