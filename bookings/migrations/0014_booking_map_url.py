# Generated by Django 5.1.2 on 2024-12-28 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0013_booking_starting_point_alter_booking_driver_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="map_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
