# Generated by Django 4.2.7 on 2023-11-24 16:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_pending_transaction_is_settled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pending_transaction',
            old_name='eventTime',
            new_name='initialTime',
        ),
        migrations.RenameField(
            model_name='settled_transaction',
            old_name='eventTime',
            new_name='finalTime',
        ),
        migrations.AddField(
            model_name='pending_transaction',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='settled_transaction',
            name='initialTime',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
