# Generated by Django 3.0.5 on 2020-04-12 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0007_auto_20200412_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation',
            name='allocateDT',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 12, 18, 50, 20, 747966)),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='allocateDT',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 12, 18, 50, 20, 748357)),
        ),
    ]
