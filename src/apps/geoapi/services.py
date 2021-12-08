from dataclasses import asdict
from typing import Any

import dacite
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from requests import Response
from rest_framework import serializers

from src.apps.geoapi.entities.ip_address import IPAddressEntity
from src.apps.geoapi.exceptions import GeoAPIException
from src.apps.geoapi.models import IPAddress, IPAddressLocation, Language


class GeoAPIService:
    """
    Service class responsible for requesting ipstack.com and saving retrieved data to database
    If provided IP address is present in database, update its properties.
    Location's languages are created only if they don't exist.
    """

    _base_url = "http://api.ipstack.com/{}"
    _entity_class = IPAddressEntity
    _error_messages = {
        "invalid_response": "Validation error while parsing ipstack.com response",
        "invalid_access_key": "Invalid ipstack access_key environment variable",
    }

    @classmethod
    def _get_url(cls, ip_address: str) -> str:
        return cls._base_url.format(ip_address)

    @classmethod
    def _get_response(cls, url: str) -> Response:
        try:
            response = requests.get(url, params={"access_key": settings.GEOAPI_KEY})
            response.raise_for_status()
        except requests.RequestException:
            raise GeoAPIException

        # API puts into body "success" bool property instead of returning 4xx status code in case
        # of invalid api_key
        if not response.json().get("success", True):
            raise GeoAPIException(detail=cls._error_messages["invalid_access_key"])

        return response

    @classmethod
    def _get_ip_address_entity(cls, response: Response) -> IPAddressEntity:
        try:
            return dacite.from_dict(data_class=cls._entity_class, data=response.json())
        except dacite.WrongTypeError:
            raise serializers.ValidationError(detail=cls._error_messages["invalid_response"])

    @classmethod
    def _create_languages(cls, location: IPAddressLocation, data: list[dict[str, Any]]) -> None:
        language_codes = {language["code"] for language in data}
        existing_language_codes = set(Language.objects.values_list("code", flat=True))
        not_existing_language_codes = language_codes - existing_language_codes

        not_existing_languages = [
            Language(**language) for language in data if language["code"] in not_existing_language_codes
        ]
        Language.objects.bulk_create(not_existing_languages)

        languages = Language.objects.filter(code__in=language_codes)
        location.languages.set(languages, clear=True)

    @classmethod
    def _create_location(cls, ip_address: IPAddress, data: dict[str, Any]) -> None:
        languages_data = data.pop("languages")
        location, _ = IPAddressLocation.objects.update_or_create(ip_address=ip_address, defaults=data)

        cls._create_languages(location=location, data=languages_data)

    @classmethod
    def _create_ip_address(cls, user: User, entity: IPAddressEntity) -> IPAddress:
        ip_address_data = asdict(entity)
        ip = ip_address_data.pop("ip")
        location_data = ip_address_data.pop("location")

        ip_address, _ = IPAddress.objects.update_or_create(ip=ip, user=user, defaults=ip_address_data)
        cls._create_location(ip_address=ip_address, data=location_data)

        return ip_address

    @classmethod
    @transaction.atomic
    def create_ip_address_location(cls, user: User, ip: str) -> IPAddress:
        url = cls._get_url(ip_address=ip)
        response = cls._get_response(url=url)
        ip_address_entity = cls._get_ip_address_entity(response=response)
        return cls._create_ip_address(user=user, entity=ip_address_entity)
