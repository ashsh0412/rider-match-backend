# Generated by Django 5.1.2 on 2024-12-28 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0015_alter_booking_driver_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="map_url",
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
    ]