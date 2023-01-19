ROOT_URLCONF = "tiser_proj.urls"

WSGI_APPLICATION = "tiser_proj.wsgi.application"

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.TiserUser"
