# Generated by Django 5.1.2 on 2024-11-05 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="user",
        ),
        migrations.AddField(
            model_name="location",
            name="first_name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="location",
            name="last_name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
