# Generated by Django 5.1.3 on 2025-01-28 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile',
            field=models.URLField(blank=True, default='https://banner2.cleanpng.com/20180419/ute/avfy9wfv6.webp', null=True),
        ),
    ]
