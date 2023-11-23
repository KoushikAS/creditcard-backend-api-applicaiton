# Generated by Django 4.2.7 on 2023-11-23 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_credit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Settled_Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txnId', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('eventTime', models.CharField(max_length=100)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.user')),
            ],
        ),
        migrations.CreateModel(
            name='Pending_Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txnId', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('eventTime', models.CharField(max_length=100)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.user')),
            ],
        ),
    ]
