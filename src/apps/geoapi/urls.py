from rest_framework.routers import DefaultRouter

from src.apps.geoapi.views import IPAddressViewSet

router = DefaultRouter()
router.register("ip-addresses", IPAddressViewSet, basename="ip_address")

app_name = "geoapi"

urlpatterns = router.urls
