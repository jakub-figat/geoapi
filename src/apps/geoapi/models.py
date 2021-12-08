from django.contrib.auth.models import User
from django.db import models

from src.apps.geoapi.managers import IPAddressQuerySet


class IPAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ip_addresses")
    ip = models.GenericIPAddressField()
    type = models.CharField(max_length=8)
    continent_code = models.CharField(max_length=10)
    continent_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=30)
    region_code = models.CharField(max_length=20)
    region_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()

    objects = IPAddressQuerySet.as_manager()


class IPAddressLocation(models.Model):
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE, related_name="location")
    geoname_id = models.IntegerField()
    capital = models.CharField(max_length=50)
    country_flag = models.URLField()
    country_flag_emoji = models.CharField(max_length=20)
    country_flag_emoji_unicode = models.CharField(max_length=40)
    calling_code = models.CharField(max_length=20)
    is_eu = models.BooleanField(default=False)
    languages = models.ManyToManyField("geoapi.Language", related_name="locations")


class Language(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    native = models.CharField(max_length=100)
