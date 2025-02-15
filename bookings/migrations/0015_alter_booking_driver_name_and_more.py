# Generated by Django 5.1.2 on 2024-12-28 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0014_booking_map_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="driver_name",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="starting_point",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
