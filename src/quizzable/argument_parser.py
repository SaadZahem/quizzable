from argparse import ArgumentParser


class CustomArgumentParser(ArgumentParser):
    def __init__(self):
        super().__init__(
            prog="Quizzable",
            description="A website for sharing quizzes",
            epilog="Made by Saad Zahem",
        )
        self.add_argument(
            "-p",
            "--port",
            type=int,
            default=8080,
            help="the port number",
        )
