import datetime as dt

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": dt.timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": dt.timedelta(days=7),
}
