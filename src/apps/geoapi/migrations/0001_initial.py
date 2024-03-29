# Generated by Django 3.2.9 on 2021-12-07 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IPAddress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ip", models.GenericIPAddressField()),
                ("type", models.CharField(max_length=8)),
                ("continent_code", models.CharField(max_length=10)),
                ("continent_name", models.CharField(max_length=30)),
                ("country_code", models.CharField(max_length=30)),
                ("region_code", models.CharField(max_length=20)),
                ("region_name", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("zip", models.CharField(max_length=30)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=5)),
                ("name", models.CharField(max_length=100)),
                ("native", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="IPAddressLocation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("geoname_id", models.IntegerField()),
                ("capital", models.CharField(max_length=50)),
                ("country_flag", models.URLField()),
                ("country_flag_emoji", models.CharField(max_length=20)),
                ("country_flag_emoji_unicode", models.CharField(max_length=40)),
                ("calling_code", models.CharField(max_length=20)),
                ("is_eu", models.BooleanField(default=False)),
                (
                    "ip_address",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="location", to="geoapi.ipaddress"
                    ),
                ),
                ("languages", models.ManyToManyField(related_name="locations", to="geoapi.Language")),
            ],
        ),
    ]
