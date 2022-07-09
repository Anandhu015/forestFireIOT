# Generated by Django 4.0.4 on 2022-07-09 04:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_sensor_alert_values_alter_alert_notify_alert_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor_alert_values',
            name='device_id1',
        ),
        migrations.RemoveField(
            model_name='sensor_alert_values',
            name='device_status1',
        ),
        migrations.RemoveField(
            model_name='sensor_alert_values',
            name='gas_analog_reading1',
        ),
        migrations.RemoveField(
            model_name='sensor_alert_values',
            name='hum_reading1',
        ),
        migrations.RemoveField(
            model_name='sensor_alert_values',
            name='temp_reading1',
        ),
        migrations.AlterField(
            model_name='alert_notify',
            name='alert_time',
            field=models.TimeField(default=datetime.datetime(2022, 7, 9, 10, 9, 45, 391205)),
        ),
    ]