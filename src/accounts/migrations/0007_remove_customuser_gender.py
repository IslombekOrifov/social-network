# Generated by Django 4.2 on 2023-07-20 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customuser_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='gender',
        ),
    ]
