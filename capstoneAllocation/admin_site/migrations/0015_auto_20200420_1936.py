# Generated by Django 3.0.5 on 2020-04-20 11:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0014_auto_20200420_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllocPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('savedDT', models.DateTimeField(default=datetime.datetime(2020, 4, 20, 19, 36, 18, 693263))),
                ('lvl', models.FloatField(null=True)),
                ('alloc', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='allocation',
            name='allocateDT',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 20, 19, 36, 18, 692260)),
        ),
    ]
