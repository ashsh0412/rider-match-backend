# Generated by Django 5.1.2 on 2024-12-29 23:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0016_alter_booking_map_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="departure_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
