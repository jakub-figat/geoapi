from unittest.mock import patch

import requests
import requests_mock
from django.contrib.auth.models import User
from django.test import TestCase

from src.apps.geoapi.exceptions import GeoAPIException
from src.apps.geoapi.models import IPAddress, IPAddressLocation, Language
from src.apps.geoapi.services import GeoAPIService


class TestGeoAPIService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="TestUser")
        cls.service_class = GeoAPIService
        cls.ip_address_data = {
            "ip": "1.1.1.1",
            "type": "ipv4",
            "continent_code": "OC",
            "continent_name": "Oceania",
            "country_code": "AU",
            "region_code": "NSW",
            "region_name": "New South Wales",
            "city": "Sydney",
            "zip": "2000",
            "latitude": -33.86714172363281,
            "longitude": 151.2071075439453,
            "location": {
                "geoname_id": 2147714,
                "capital": "Canberra",
                "country_flag": "https://assets.ipstack.com/flags/au.svg",
                "country_flag_emoji": "🇦🇺",
                "country_flag_emoji_unicode": "U+1F1E6 U+1F1FA",
                "calling_code": "61",
                "is_eu": False,
                "languages": [
                    {"code": "en", "name": "English", "native": "English"},
                ],
            },
        }

        cls.modified_ip_address_data = {
            "ip": "1.1.1.1",
            "type": "ipv4",
            "continent_code": "PL",
            "continent_name": "Europe",
            "country_code": "PL",
            "region_code": "NSW",
            "region_name": "New South Wales",
            "city": "Sydney",
            "zip": "2000",
            "latitude": -33.86714172363281,
            "longitude": 151.2071075439453,
            "location": {
                "geoname_id": 2147714,
                "capital": "Warsaw",
                "country_flag": "https://assets.ipstack.com/flags/au.svg",
                "country_flag_emoji": "🇦🇺",
                "country_flag_emoji_unicode": "U+1F1E6 U+1F1FA",
                "calling_code": "61",
                "is_eu": True,
                "languages": [
                    {"code": "pl", "name": "Polish", "native": "Polski"},
                ],
            },
        }

        cls.ip = cls.ip_address_data["ip"]
        cls.ip_url = cls.service_class._base_url.format(cls.ip)

        cls.invalid_access_key_response = {
            "success": False,
            "error": {
                "code": 101,
                "type": "invalid_access_key",
                "info": "You have not supplied a valid API Access Key. [Technical Support: support@apilayer.com]",
            },
        }

    @requests_mock.Mocker()
    def test_geoapi_service_correctly_creates_ip_address(self, requests_mocker):
        requests_mocker.get(self.ip_url, json=self.ip_address_data)

        ip_address = self.service_class.create_ip_address_location(user=self.user, ip=self.ip)
        language_code = self.ip_address_data["location"]["languages"][0]["code"]

        self.assertEqual(ip_address.ip, self.ip)
        self.assertEqual(IPAddressLocation.objects.filter(ip_address=ip_address).count(), 1)
        self.assertEqual(Language.objects.filter(code=language_code).count(), 1)

    @requests_mock.Mocker()
    def test_geoapi_correctly_updates_ip_address_if_exists(self, requests_mocker):
        requests_mocker.get(self.ip_url, json=self.ip_address_data)
        self.service_class.create_ip_address_location(user=self.user, ip=self.ip)

        requests_mocker.get(self.ip_url, json=self.modified_ip_address_data)
        ip_address = self.service_class.create_ip_address_location(user=self.user, ip=self.ip)
        language_code = self.modified_ip_address_data["location"]["languages"][0]["code"]

        self.assertEqual(ip_address.ip, self.ip)
        self.assertEqual(ip_address.continent_code, self.modified_ip_address_data["continent_code"])
        self.assertEqual(IPAddress.objects.count(), 1)

        self.assertEqual(ip_address.location.capital, self.modified_ip_address_data["location"]["capital"])
        self.assertEqual(Language.objects.filter(code=language_code).count(), 1)

    @requests_mock.Mocker()
    def test_geoapi_service_raises_exception_in_case_of_wrong_access_key(self, requests_mocker):
        requests_mocker.get(self.ip_url, json=self.invalid_access_key_response)

        with self.assertRaisesMessage(
            expected_exception=GeoAPIException,
            expected_message=self.service_class._error_messages["invalid_access_key"],
        ):
            self.service_class.create_ip_address_location(user=self.user, ip=self.ip)

    @requests_mock.Mocker()
    def test_geoapi_service_does_not_create_duplicated_languages(self, requests_mocker):
        requests_mocker.get(self.ip_url, json=self.ip_address_data)

        language_data = self.ip_address_data["location"]["languages"][0]
        Language.objects.create(**language_data)
        ip_address = self.service_class.create_ip_address_location(user=self.user, ip=self.ip)

        self.assertEqual(ip_address.location.languages.count(), 1)
        self.assertEqual(Language.objects.count(), 1)

    @patch("requests.get")
    def test_geoapi_serivce_raises_exception_in_case_of_requests_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException

        with self.assertRaises(expected_exception=GeoAPIException):
            self.service_class.create_ip_address_location(user=self.user, ip=self.ip)
