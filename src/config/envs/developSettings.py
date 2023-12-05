from .settings import *
AUTH_USER_MODEL='accounts.User'

#REST settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


CORS_ALLOW_ALL_ORIGINS=True