# Generated by Django 4.0.4 on 2022-06-27 17:54

from django.db import migrations, models
import sqlalchemy.sql.expression


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_secondsensor_reading_device_status1'),
    ]

    operations = [
        migrations.CreateModel(
            name='login',
            fields=[
                ('user_id', models.IntegerField(primary_key=sqlalchemy.sql.expression.true, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
