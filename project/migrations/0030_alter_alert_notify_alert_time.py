# Generated by Django 4.0.4 on 2022-07-09 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_alter_alert_notify_alert_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert_notify',
            name='alert_time',
            field=models.TimeField(default='13:10:21'),
        ),
    ]
