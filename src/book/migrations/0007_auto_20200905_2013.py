# Generated by Django 2.2.14 on 2020-09-05 20:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20200905_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrent',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='This price should not be affected after rent started', max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]
