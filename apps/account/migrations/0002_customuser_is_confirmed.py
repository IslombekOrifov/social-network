# Generated by Django 5.2 on 2025-05-04 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_confirmed",
            field=models.BooleanField(default=False),
        ),
    ]
