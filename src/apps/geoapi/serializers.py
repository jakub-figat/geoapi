from rest_framework import serializers

from src.apps.geoapi.models import IPAddress, IPAddressLocation, Language


class IPAddressInputSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class LanguageOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            "code",
            "name",
            "native",
        )
        read_only_fields = fields


class IPAddressLocationOutputSerializer(serializers.ModelSerializer):
    languages = LanguageOutputSerializer(many=True, read_only=True)

    class Meta:
        model = IPAddressLocation
        fields = (
            "ip_address",
            "geoname_id",
            "capital",
            "country_flag",
            "country_flag_emoji",
            "country_flag_emoji_unicode",
            "calling_code",
            "is_eu",
            "languages",
        )
        read_only_fields = fields


class IPAddressOutputSerializer(serializers.ModelSerializer):
    location = IPAddressLocationOutputSerializer(read_only=True)

    class Meta:
        model = IPAddress
        fields = (
            "id",
            "ip",
            "type",
            "continent_code",
            "continent_name",
            "country_code",
            "region_code",
            "region_name",
            "city",
            "zip",
            "latitude",
            "longitude",
            "location",
        )
        read_only_fields = fields
