# Generated by Django 4.2.7 on 2024-01-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
