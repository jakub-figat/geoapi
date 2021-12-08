from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.geoapi.models import IPAddress, IPAddressLocation, Language


class TestGeoAPIViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ip_address_list_url = reverse("geoapi:ip-address-list")
        cls.user = User.objects.create(username="TestUser")
        cls.other_user = User.objects.create(username="Other")

        cls.ip_address = IPAddress.objects.create(
            user=cls.user,
            ip="5.5.5.5",
            type="ipv4",
            continent_code="AF",
            continent_name="Test",
            country_code="TT",
            region_code="Tes",
            region_name="Test",
            city="Test",
            zip="2000",
            latitude=-33.86714172363281,
            longitude=151.2071075439453,
        )

        cls.ip_address_detail_url = reverse("geoapi:ip-address-detail", kwargs={"pk": cls.ip_address.pk})

        cls.language_pl = Language.objects.create(
            code="pl",
            name="Polish",
            native="Polski",
        )

        cls.location = IPAddressLocation.objects.create(
            ip_address=cls.ip_address,
            geoname_id=2147714,
            capital="Canberra",
            country_flag="https://assets.ipstack.com/flags/au.svg",
            country_flag_emoji="🇦🇺",
            country_flag_emoji_unicode="U+1F1E6 U+1F1FA",
            calling_code="61",
            is_eu=False,
        )
        cls.location.languages.add(cls.language_pl)

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_user_can_retrieve_his_ip_addresses(self):
        response = self.client.get(self.ip_address_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 1)
        ip_address_data = response.data["results"][0]

        self.assertEqual(ip_address_data["ip"], self.ip_address.ip)
        self.assertEqual(ip_address_data["location"]["geoname_id"], self.location.geoname_id)

    def test_user_can_retrieve_ip_address_by_id(self):
        response = self.client.get(self.ip_address_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_his_ip_address(self):
        response = self.client.delete(self.ip_address_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(IPAddress.objects.filter(user=self.user).exists())

    def test_other_user_cannot_delete_other_user_ip_address(self):
        self.client.force_login(user=self.other_user)
        response = self.client.delete(self.ip_address_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(IPAddress.objects.filter(user=self.user).exists())

    def test_anonymous_user_cannot_retrieve_ip_addresses(self):
        self.client.logout()
        response = self.client.get(self.ip_address_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_delete_ip_addresses(self):
        self.client.logout()
        response = self.client.delete(self.ip_address_detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(IPAddress.objects.filter(user=self.user).exists())
