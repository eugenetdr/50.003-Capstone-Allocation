# Generated by Django 3.0.5 on 2020-04-21 15:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0017_auto_20200420_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocation',
            name='lvl',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='allocation',
            name='allocateDT',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 21, 23, 6, 11, 831566)),
        ),
    ]