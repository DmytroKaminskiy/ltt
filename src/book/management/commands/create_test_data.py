from book.models import Book, BookRent, Category, RentDayHistory

from django.core.management.base import BaseCommand

from faker import Faker


class Command(BaseCommand):
    help = 'Generates test data (books).'  # noqa A003

    def handle(self, *args, **options):
        Book.objects.all().delete()
        BookRent.objects.all().delete()
        RentDayHistory.objects.all().delete()

        fake = Faker()
        Book.objects.bulk_create([
            Book(title=fake.sentence(),
                 category=Category.objects.order_by('?').last())
            for _ in range(10_000)
        ])
