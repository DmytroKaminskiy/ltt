# Generated by Django 2.2.14 on 2020-09-06 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_auto_20200906_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]