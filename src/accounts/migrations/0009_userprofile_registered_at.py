# Generated by Django 4.2.7 on 2024-01-31 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_type_alter_userprofile_husband'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='registered_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]