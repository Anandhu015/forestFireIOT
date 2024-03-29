# Generated by Django 4.0.4 on 2022-06-21 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='secondSensor_reading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id1', models.IntegerField(max_length=20)),
                ('temp_reading1', models.FloatField(max_length=20)),
                ('hum_reading1', models.FloatField(max_length=20)),
                ('device_status1', models.BooleanField(default=True)),
                ('gas_analog_reading1', models.FloatField(default='0', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor_reading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.IntegerField(max_length=20)),
                ('temp_reading', models.FloatField(max_length=20)),
                ('hum_reading', models.FloatField(max_length=20)),
                ('device_status', models.BooleanField(default=True)),
                ('gas_analog_reading', models.FloatField(default='0', max_length=20)),
            ],
        ),
    ]
