# Generated by Django 4.2 on 2023-08-07 14:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_customuser_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='fol',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
