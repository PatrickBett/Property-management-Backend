# Generated by Django 5.1.3 on 2024-12-03 00:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='name',
            field=models.ForeignKey(limit_choices_to={'role': 'tenant'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
