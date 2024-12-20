# Generated by Django 4.2.7 on 2024-01-11 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='Regional_Municipality',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='boys',
        ),
        migrations.RemoveField(
            model_name='user',
            name='education',
        ),
        migrations.RemoveField(
            model_name='user',
            name='father_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='field_study',
        ),
        migrations.RemoveField(
            model_name='user',
            name='girls',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='job',
        ),
        migrations.RemoveField(
            model_name='user',
            name='office_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='telephone',
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'FATHER'), (2, 'MOTHER')], null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
