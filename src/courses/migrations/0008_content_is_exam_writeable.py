# Generated by Django 4.2.7 on 2024-01-05 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_courseinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='is_exam_writeable',
            field=models.BooleanField(default=False),
        ),
    ]