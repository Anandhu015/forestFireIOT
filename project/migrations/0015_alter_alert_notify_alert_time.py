# Generated by Django 4.0.4 on 2022-07-03 16:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_alter_alert_notify_alert_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert_notify',
            name='alert_time',
            field=models.TimeField(default=datetime.datetime(2022, 7, 3, 21, 32, 51, 867078)),
        ),
    ]
