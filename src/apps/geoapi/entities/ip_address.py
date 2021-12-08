from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageEntity:
    code: str
    name: str
    native: str


@dataclass(frozen=True)
class LocationEntity:
    geoname_id: int
    capital: str
    country_flag: str
    country_flag_emoji: str
    country_flag_emoji_unicode: str
    calling_code: str
    is_eu: bool
    languages: list[LanguageEntity]


@dataclass(frozen=True)
class IPAddressEntity:
    ip: str
    type: str
    continent_code: str
    continent_name: str
    country_code: str
    region_code: str
    region_name: str
    city: str
    zip: str
    latitude: float
    longitude: float
    location: LocationEntity
