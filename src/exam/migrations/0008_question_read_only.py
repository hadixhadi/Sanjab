# Generated by Django 4.2.7 on 2024-01-05 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_alter_question_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='read_only',
            field=models.BooleanField(default=True),
        ),
    ]