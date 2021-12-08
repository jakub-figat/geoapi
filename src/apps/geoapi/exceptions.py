from rest_framework import status
from rest_framework.exceptions import APIException


class GeoAPIException(APIException):
    default_code = "error"
    default_detail = "Something went wrong when requesting ipstack.com"
    status_code = status.HTTP_400_BAD_REQUEST
