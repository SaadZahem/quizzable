import pytest

from quizzable.services import qy


def _valid_question():
    return {"q": "Q?", "a": "1", "b": "2", "c": "3", "d": "4", "k": "a"}


def test_validate_accepts_complete_question():
    question = _valid_question()
    assert qy.validate(question) is question


def test_validate_allows_missing_optional_choice_e():
    # 'e' is optional and should not be required by validate
    assert qy.validate(_valid_question()) is not None


@pytest.mark.parametrize("key", ["q", "a", "b", "c", "d", "k"])
def test_validate_rejects_missing_required_key(key):
    question = _valid_question()
    del question[key]
    with pytest.raises(KeyError):
        qy.validate(question)


@pytest.mark.parametrize("key", ["q", "a", "b", "c", "d", "k"])
def test_validate_rejects_empty_required_value(key):
    question = _valid_question()
    question[key] = ""
    with pytest.raises(AssertionError):
        qy.validate(question)
