from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class IPAddressLocationAPIView(GenericAPIView):
    def post(self, request: Request, ip_address: str) -> Response:
        pass
