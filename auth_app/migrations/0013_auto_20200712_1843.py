# Generated by Django 3.0.8 on 2020-07-12 13:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0012_auto_20200712_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
