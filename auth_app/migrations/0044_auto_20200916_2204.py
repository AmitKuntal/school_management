# Generated by Django 3.0.8 on 2020-09-16 16:34

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0043_auto_20200915_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='testid',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 9, 16)),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='attendancedate',
            field=models.DateField(default=datetime.date(2020, 9, 16)),
        ),
        migrations.AlterField(
            model_name='homework',
            name='homeworkdate',
            field=models.DateField(default=datetime.date(2020, 9, 16)),
        ),
        migrations.AlterField(
            model_name='test',
            name='expiredate',
            field=models.DateField(default=datetime.date(2020, 9, 16)),
        ),
    ]