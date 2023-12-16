# Generated by Django 4.2.7 on 2023-12-16 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('national_code', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('type', models.SmallIntegerField(blank=True, choices=[(1, 'FATHER'), (2, 'MOTHER')], null=True)),
                ('father_name', models.CharField(blank=True, max_length=200, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('education', models.CharField(blank=True, max_length=200, null=True)),
                ('field_study', models.CharField(blank=True, max_length=200, null=True)),
                ('telephone', models.CharField(blank=True, max_length=11, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('Regional_Municipality', models.SmallIntegerField(blank=True, null=True)),
                ('job', models.CharField(blank=True, max_length=200, null=True)),
                ('office_address', models.CharField(blank=True, max_length=200, null=True)),
                ('boys', models.SmallIntegerField(blank=True, null=True)),
                ('girls', models.SmallIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('phone_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('postal_code', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('code', models.PositiveSmallIntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expire_at', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChildUser',
            fields=[
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('national_code', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('birth_date', models.DateField()),
                ('grade', models.CharField(max_length=50)),
                ('school_address', models.CharField(max_length=100)),
                ('father', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='father_child', to=settings.AUTH_USER_MODEL)),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mother_child', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
