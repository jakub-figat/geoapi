from dataclasses import asdict
from typing import Any

import dacite
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from requests import Response
from rest_framework.serializers import ValidationError

from src.apps.geoapi.entities.ip_address import IPAddressEntity
from src.apps.geoapi.exceptions import GeoAPIException
from src.apps.geoapi.models import IPAddress, IPAddressLocation, Language


class GeoAPIService:
    _base_url = "http://api.ipstack.com/{}"
    _entity_class = IPAddressEntity
    _error_messages = {"invalid_response": {"detail": "Validation error while parsing ipstack.com response"}}

    @classmethod
    def _get_url(cls, ip_address: str) -> str:
        return cls._base_url.format(ip_address)

    @classmethod
    def _get_response(cls, url: str) -> Response:
        try:
            response = requests.post(url, params={"access_key": settings.GEOAPI_KEY})
            response.raise_for_status()
        except requests.RequestException:
            raise GeoAPIException

        return response

    @classmethod
    def _get_ip_address_entity(cls, response: Response) -> IPAddressEntity:
        try:
            return dacite.from_dict(data_class=cls._entity_class, data=response.json())
        except dacite.WrongTypeError:
            raise ValidationError(cls._error_messages["invalid_response"])

    @classmethod
    def _create_languages(cls, location: IPAddressLocation, data: list[dict[str, Any]]) -> None:
        language_codes = {language["code"] for language in data}
        existing_language_codes = set(Language.objects.values_list("code", flat=True))
        not_existing_language_codes = language_codes - existing_language_codes

        not_existing_languages = [Language(**language) for language in not_existing_language_codes]
        Language.objects.bulk_create(not_existing_languages)

        languages = Language.objects.filter(code__in=language_codes)
        location.languages.set(languages)

    @classmethod
    def _create_location(cls, ip_address: IPAddress, data: dict[str, Any]) -> None:
        languages_data = data.pop("languages")
        location = IPAddressLocation.objects.create(ip_address=ip_address, **data)

        cls._create_languages(location=location, data=languages_data)

    @classmethod
    def _create_ip_address(cls, user: User, entity: IPAddressEntity) -> IPAddress:
        ip_address_data = asdict(entity)
        location_data = ip_address_data.pop("location")

        ip_address = IPAddress.objects.create(user=user, **ip_address_data)
        cls._create_location(ip_address=ip_address, data=location_data)

        return ip_address

    @classmethod
    @transaction.atomic
    def create_ip_address_location(cls, user: User, ip: str) -> IPAddress:
        url = cls._get_url(ip_address=ip)
        response = cls._get_response(url=url)
        ip_address_entity = cls._get_ip_address_entity(response=response)
        return cls._create_ip_address(user=user, entity=ip_address_entity)
