# Generated by Django 3.0.5 on 2020-04-12 09:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0006_allocation_cluster'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='clusAngle',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cluster',
            name='clusLvl',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cluster',
            name='industry',
            field=models.CharField(default='default', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cluster',
            name='projectName',
            field=models.CharField(default='default', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cluster',
            name='sLength',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cluster',
            name='sWidth',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='reqdata',
            name='industry',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='allocation',
            name='allocateDT',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 12, 17, 28, 49, 31677)),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='allocateDT',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 12, 17, 28, 49, 32089)),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='teamID',
            field=models.CharField(max_length=100),
        ),
    ]
