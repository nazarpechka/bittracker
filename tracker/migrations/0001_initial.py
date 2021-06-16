# Generated by Django 3.2.4 on 2021-06-08 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('symbol', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=1024)),
                ('secret', models.CharField(max_length=1024)),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.exchange')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fiat',
            fields=[
                ('symbol', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.crypto')),
                ('fiat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.fiat')),
            ],
        ),
        migrations.CreateModel(
            name='ManualBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.crypto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExchangeBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.crypto')),
                ('exchange_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.exchangeaccount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]