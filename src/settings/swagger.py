SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization: Bearer <jwtToken>",
            "in": "header",
        },
    },
    "LOGIN_URL": "/api/login/",
    "LOGOUT_URL": "/api/logout/",
}
