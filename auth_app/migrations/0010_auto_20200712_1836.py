# Generated by Django 3.0.8 on 2020-07-12 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0009_auto_20200712_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='id',
            field=models.CharField(default='8a0ee568-c440-11ea-b31c-402343e1102e', editable=False, max_length=200, primary_key=True, serialize=False),
        ),
    ]
