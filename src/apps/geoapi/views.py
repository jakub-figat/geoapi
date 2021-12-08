from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.apps.geoapi.models import IPAddress
from src.apps.geoapi.serializers import IPAddressInputSerializer, IPAddressOutputSerializer
from src.apps.geoapi.services import GeoAPIService


class IPAddressViewSet(ModelViewSet):
    serializer_class = IPAddressOutputSerializer
    http_method_names = ["get", "post", "delete"]
    service_class = GeoAPIService

    def get_queryset(self):
        return (
            IPAddress.objects.related_with_user(user=self.request.user)
            .select_related("location")
            .prefetch_related("location__languages")
        )

    @swagger_auto_schema(request_body=IPAddressInputSerializer)
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = IPAddressInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_address = self.service_class.create_ip_address_location(user=request.user, **serializer.validated_data)
        return Response(self.get_serializer(ip_address).data, status=status.HTTP_201_CREATED)
