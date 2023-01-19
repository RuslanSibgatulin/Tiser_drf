import os
from pathlib import Path

from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DJANGO_DEBUG", False) == "True"

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
        "OPTIONS": {
            # Нужно явно указать схемы, с которыми будет работать приложение.
            "options": "-c search_path=public,content"
        },
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
