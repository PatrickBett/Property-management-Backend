# Generated by Django 5.1.3 on 2025-03-15 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_messages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myhome',
            old_name='tenant',
            new_name='user',
        ),
    ]
