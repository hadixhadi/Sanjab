# Generated by Django 4.2.7 on 2024-01-04 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_content_is_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoContents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('url', models.URLField(max_length=300)),
            ],
        ),
    ]