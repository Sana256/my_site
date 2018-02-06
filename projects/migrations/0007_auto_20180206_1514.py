# Generated by Django 2.0.1 on 2018-02-06 12:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20180206_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='elapsed_time',
            field=models.DurationField(default=datetime.timedelta(0), null=True),
        ),
        migrations.AlterField(
            model_name='workday',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
