import os
from pathlib import Path

from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "debug")

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

include(
    "settings/common.py",
    "settings/logger.py",
    "settings/middleware.py",
    "settings/templates.py",
    "settings/auth.py",
    "settings/apps.py",
    "settings/rest.py",
)
