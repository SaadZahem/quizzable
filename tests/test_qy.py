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


# --- parse_document -------------------------------------------------------


def test_parse_document_bare_list_has_no_title_or_tags():
    questions = [_valid_question()]
    title, tags, parsed = qy.parse_document(questions)
    assert title is None
    assert tags == ""
    assert parsed is questions


def test_parse_document_mapping_title_is_used():
    data = {"title": "Custom Title", "questions": [_valid_question()]}
    title, _, _ = qy.parse_document(data)
    assert title == "Custom Title"


def test_parse_document_blank_title_becomes_none():
    data = {"title": "   ", "questions": [_valid_question()]}
    title, _, _ = qy.parse_document(data)
    assert title is None


def test_parse_document_tags_list_stored_newline_separated():
    data = {"tags": ["cardiology", "week 3"], "questions": [_valid_question()]}
    _, tags, _ = qy.parse_document(data)
    assert tags == "cardiology\nweek 3"


def test_parse_document_tags_single_string_accepted():
    data = {"tags": "solo", "questions": [_valid_question()]}
    _, tags, _ = qy.parse_document(data)
    assert tags == "solo"


def test_parse_document_tags_blank_entries_dropped():
    data = {"tags": ["  ", "kept", ""], "questions": [_valid_question()]}
    _, tags, _ = qy.parse_document(data)
    assert tags == "kept"


@pytest.mark.parametrize("data", [None, [], {}, {"questions": []}, {"title": "x"}])
def test_parse_document_rejects_missing_questions(data):
    with pytest.raises(qy.InvalidQuizFile):
        qy.parse_document(data)
