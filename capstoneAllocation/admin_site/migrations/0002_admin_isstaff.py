# Generated by Django 3.0.3 on 2020-03-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='isStaff',
            field=models.IntegerField(default=1),
        ),
    ]
