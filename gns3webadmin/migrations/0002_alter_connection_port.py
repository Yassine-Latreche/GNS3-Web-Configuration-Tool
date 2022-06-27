# Generated by Django 4.0.4 on 2022-05-14 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gns3webadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='port',
            field=models.PositiveIntegerField(default=3080, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)]),
        ),
    ]