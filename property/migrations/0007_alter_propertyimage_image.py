# Generated by Django 5.1.3 on 2025-04-02 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_propertyimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
