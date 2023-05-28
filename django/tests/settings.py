"""Override Django settings for tests."""

# pylint: disable=unused-wildcard-import,wildcard-import
from pieskiUW.settings import *

# Use sqlite3 for tests. It is faster than remote postgresql instance.
# It provides better separation between development and deployment.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "tests/test_data/db.sqlite3",
        "ATOMIC_REQUESTS": True,
    }
}
