# Generated by Django 3.0.8 on 2020-08-03 17:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0032_auto_20200802_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 8, 3)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 8, 3)),
        ),
    ]
