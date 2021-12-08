from decouple import config

DEBUG = False

ALLOWED_HOSTS = ["localhost", config("ALLOWED_HOST")]
