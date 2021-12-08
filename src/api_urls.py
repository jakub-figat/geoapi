from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("", include("src.apps.geoapi.urls")),
    path("users/", include("src.apps.user.urls")),
]

if settings.DEBUG:
    from src.swagger import schema_view

    urlpatterns += [path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")]
