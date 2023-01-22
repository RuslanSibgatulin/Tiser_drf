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
    "components/common.py",
    "components/logger.py",
    "components/middleware.py",
    "components/templates.py",
    "components/auth.py",
    "components/apps.py",
    "components/rest.py",
)
