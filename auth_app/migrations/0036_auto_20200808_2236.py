# Generated by Django 3.0.8 on 2020-08-08 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0035_auto_20200805_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 8, 8)),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 8, 8)),
        ),
        migrations.AlterField(
            model_name='homework',
            name='homeworkdate',
            field=models.DateField(default=datetime.date(2020, 8, 8)),
        ),
    ]