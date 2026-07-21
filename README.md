## Running the project

    uv add -r requirements.txt
    uv pip install -e .
    source .venv/bin/activate
    python -m quizzable.app

### Running in production (without reload)

    uv add -r requirements.txt
    uv pip install .
    source .venv/bin/activate
    python -m quizzable
