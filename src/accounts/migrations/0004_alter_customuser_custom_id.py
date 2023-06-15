# Generated by Django 4.2 on 2023-06-15 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_life_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='custom_id',
            field=models.CharField(db_index=True, error_messages={'unique': 'A user with that custom_id already exists.'}, max_length=12, unique=True),
        ),
    ]