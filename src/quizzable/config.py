import os
import pathlib

import dotenv

if not dotenv.load_dotenv(".env"):
    raise ValueError(".env file is missing")


STORAGE_SECRET = os.getenv("STORAGE_SECRET")
"used to enable app.storage.user"

SECRET_KEY = os.getenv("SECRET_KEY")
"used to secure JWT tokens"

ALGORITHM = "HS256"
"widely used algorithm to secure JWT tokens"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
"the time after which a relogin is needed"

# Theme configuration
COLORS = dict(
    primary="#6B705C",
    secondary="#DDBEA9",
    accent="#CB997E",
    myblack="#1A1A18",
    mywhite="#FAF8F5",
    brand="hsl(39, 77%, 90%)",
)

templates_dir = pathlib.Path(__file__).with_name("templates")
