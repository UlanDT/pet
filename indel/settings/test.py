from .base import *
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = env("SECRET_KEY", default="q938jgintbniq3oj")
TEST_RUNNER = "django.test.runner.DiscoverRunner"


DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        },
    }
