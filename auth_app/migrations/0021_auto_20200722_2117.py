# Generated by Django 3.0.8 on 2020-07-22 15:47

import auth_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0020_auto_20200721_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='image',
            field=models.ImageField(upload_to=auth_app.models.upload_path),
        ),
    ]
