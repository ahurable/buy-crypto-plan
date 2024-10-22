# Generated by Django 5.0.2 on 2024-03-04 07:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customusermodel_is_active_customusermodel_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='OtpEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='otp_tab', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
