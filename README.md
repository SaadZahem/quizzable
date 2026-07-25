# Quizzable

A website for making/sharing/taking quizzes.

The app also includes an SQLite database managed by `tortoise-orm`.
The app handles simple authentication with JWT tokens and password hashing.

## Running the project

The project is structured as a package and is managed by `uv`.
There are 2 options for starting the project.

### Running for development

This option

    uv add -r requirements.txt
    uv pip install -e .
    source .venv/bin/activate
    python -m quizzable.app

### Running in production (without reload)

    uv add -r requirements.txt
    uv pip install .
    source .venv/bin/activate
    python -m quizzable

## Suplementary Scripts

The `bin/` directory houses additional scripts that aids in development.

The only script in there currently is `init.py`.
This reads quizzes data from `data/` directory and adds them to the database.
This requires the project to be first installed as a package.
