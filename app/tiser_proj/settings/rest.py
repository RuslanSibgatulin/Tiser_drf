import os

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": os.environ.get("DRF_PAGE_SIZE", 100),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ]
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "DRF Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}
