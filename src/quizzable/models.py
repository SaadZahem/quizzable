from dataclasses import dataclass

import yaml


@dataclass
class Question:
    text: str
    choices: list[str]
    correct: int
    hint: str = ""


def load_questionset(file) -> dict[int, Question]:
    with open(file, "rb") as fp:
        data = yaml.safe_load(fp)

    questions = {}
    for number, block in enumerate(data, start=1):
        question = Question(
            block["q"],
            [
                block["a"],
                block["b"],
                block["c"],
                block["d"],
                *([block["e"]] if "e" in block else ()),
            ],
            "abcde".index(block["k"]),
        )
        questions[number] = question

    return questions


if __name__ == "__main__":
    import sys
    from pprint import pprint

    qs = load_questionset(sys.argv[1])
    pprint(qs)
