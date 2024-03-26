# Generated by Django 5.0.2 on 2024-03-12 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customusermodel_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='register_method',
            field=models.CharField(choices=[('email', 'Email'), ('gmail', 'Gmail')], default='email', max_length=10),
        ),
    ]
