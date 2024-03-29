from decouple import config
from split_settings.tools import include

ENV = config("ENV", default="dev")

base_settings = [
    "common.py",
    "geoapi.py",
    "drf.py",
    "swagger.py",
    f"{ENV}.py",
]


include(*base_settings)
