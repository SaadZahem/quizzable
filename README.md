# Quizzable

A website for making/sharing/taking quizzes.

The app also includes an SQLite database managed by `tortoise-orm`.
The app handles simple authentication with JWT tokens and password hashing.

## Running the project

The project is structured as a package and is managed by `uv`.
Note that a [`.env`](#.env) file is required by this project.
The following command will set it up for you.

    bin/init_env.sh

There are 2 options for starting the project.

### Running for development

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

One script in there is `init_db.py`.
This reads quizzes data from `data/` directory and adds them to the database.
This requires the project to be first installed as a package.

Another script is `init_env.py`.
This creates a `.env` file in the current directory which is required for this project to run.

## .env

`SECRET_KEY`.
Used to hash users passwords.

`STORAGE_SECRET`.
Used to encrypt user data.
Required by `nicegui` to enable use of `app.storage.user`.
