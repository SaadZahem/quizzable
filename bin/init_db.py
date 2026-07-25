#!/usr/bin/env python

import os

import yaml
from tortoise import Tortoise, exceptions, run_async

from quizzable.models import ChoiceEnum, MCQuestion, MCQuiz, User


async def main():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"quizzable": ["quizzable.models"]}
    )
    await Tortoise.generate_schemas()

    quizzes = [
        file.removesuffix(".yml")
        for file in os.listdir("data")
        if file.endswith(".yml")
    ]

    me = await User.first()

    for quizfile in quizzes:
        with open(f"data/{quizfile}.yml", "rb") as fp:
            data = yaml.safe_load(fp)

        quizmodel = await MCQuiz.create(
            title=quizfile.replace(*"- ").title(),
            maintainer=me,
        )

        for questiondict in data:
            try:
                await MCQuestion.create(
                    text=questiondict["q"],
                    a=questiondict["a"],
                    b=questiondict["b"],
                    c=questiondict["c"],
                    d=questiondict["d"],
                    e=questiondict.get("e"),
                    correct=ChoiceEnum(questiondict["k"]),
                    quiz=quizmodel,
                )
            except exceptions.IntegrityError:
                print(questiondict)
                quit()


if __name__ == "__main__":
    run_async(main())
