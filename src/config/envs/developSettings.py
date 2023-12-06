from .settings import *
AUTH_USER_MODEL='accounts.User'

#REST settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# CORS_ORIGIN_WHITELIST = (
# "http://192.168.100.31:3000",
# "http://192.168.100.15:8000",
# )
# CSRF_TRUSTED_ORIGINS = ["http://192.168.100.31:3000"]
CORS_ALLOW_ALL_ORIGINS=True