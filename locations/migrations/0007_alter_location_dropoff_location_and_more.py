# Generated by Django 5.1.2 on 2024-12-28 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0006_alter_location_dropoff_location_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="dropoff_location",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="location",
            name="pickup_location",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
