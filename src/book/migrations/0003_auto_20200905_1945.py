# Generated by Django 2.2.14 on 2020-09-05 19:45
from decimal import Decimal

from django.db import migrations

def forwards(apps, schema_editor):
    Category = apps.get_model('book', 'Category')
    categories = (
        ('regular', '1.5'),
        ('fiction', '3.0'),
        ('novels', '1.5'),
    )
    Category.objects.bulk_create([
        Category(name=name, price=Decimal(price))
        for name, price in categories
    ])

    # update books with category regular
    Book = apps.get_model('book', 'Book')
    Book.objects.update(category_id=Category.objects.get(name='regular'))


def backwards(apps, schema_editor):
    Category = apps.get_model('book', 'Category')
    Book = apps.get_model('book', 'Book')
    Category.objects.all().delete()
    Book.objects.update(category_id=None)


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20200905_1945'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
