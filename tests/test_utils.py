from quizzable.utils import substitute, totitle


def test_totitle_replaces_hyphens_and_titlecases():
    assert totitle("my-cool-quiz") == "My Cool Quiz"


def test_totitle_single_word():
    assert totitle("physics") == "Physics"


def test_substitute_fills_known_placeholders(tmp_path):
    file = tmp_path / "template.txt"
    file.write_text("color: $primary")
    assert substitute(file, {"primary": "red"}) == "color: red"


def test_substitute_leaves_unknown_placeholders_untouched(tmp_path):
    file = tmp_path / "template.txt"
    file.write_text("$primary and $missing")
    assert substitute(file, {"primary": "red"}) == "red and $missing"
