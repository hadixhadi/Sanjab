# Generated by Django 4.2.7 on 2024-02-13 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_userprofile_registered_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_super_admin',
            field=models.BooleanField(default=False),
        ),
    ]