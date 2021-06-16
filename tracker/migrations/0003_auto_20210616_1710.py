# Generated by Django 3.2.4 on 2021-06-16 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0002_auto_20210616_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.fiat')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='exchangeaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.useraccount'),
        ),
        migrations.AlterField(
            model_name='manualbalance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.useraccount'),
        ),
    ]