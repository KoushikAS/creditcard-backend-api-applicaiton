# Generated by Django 4.2.7 on 2023-11-24 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='amount',
            new_name='balance',
        ),
    ]
