# Generated by Django 4.0.4 on 2022-07-01 22:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_remove_alert_notify_device_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert_notify',
            name='device_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='alert_notify',
            name='alert_time',
            field=models.TimeField(default=datetime.datetime(2022, 7, 2, 4, 6, 5, 449303)),
        ),
    ]
