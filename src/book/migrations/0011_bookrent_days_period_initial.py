# Generated by Django 2.2.14 on 2020-09-14 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_auto_20200906_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrent',
            name='days_period_initial',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
