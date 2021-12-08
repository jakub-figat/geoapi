from django.conf import settings
from django.urls import include, path

from src.swagger import schema_view

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("", include("src.apps.geoapi.urls")),
    path("users/", include("src.apps.user.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")]
