from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="GeoAPI", default_version="v1", description="API for retrieving geolocation data based on IP address"
    ),
    public=False,
    permission_classes=(AllowAny,),
)
