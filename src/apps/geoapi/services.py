import requests
from django.conf import settings


class GeoAPIService:
    _base_url = "http://api.ipstack.com/{}"

    def _get_url(self, ip_address: str) -> str:
        return self._base_url.format(ip_address)

    def get_ip_address_location(self, ip_address: str) -> None:
        url = self._get_url(ip_address=ip_address)
        response = requests.post(url, params={"access_key": settings.GEOAPI_KEY})
        print(response.json())
