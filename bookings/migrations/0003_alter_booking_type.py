# Generated by Django 5.1.2 on 2024-10-14 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_booking_created_at_booking_type_alter_booking_guests"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="type",
            field=models.CharField(
                choices=[("rider", "Rider"), ("driver", "Driver")],
                default="rider",
                max_length=6,
            ),
        ),
    ]
