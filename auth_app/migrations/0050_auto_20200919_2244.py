# Generated by Django 3.0.8 on 2020-09-19 17:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0049_auto_20200919_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='testid',
            field=models.CharField(default=uuid.uuid4, max_length=100),
        ),
    ]