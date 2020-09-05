import random

from account.models import User

from book import choices
from book.models import Book, BookRent, RentDayHistory

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
            Book(title=fake.sentence()) for _ in range(10_000)
        ])

        BookRent.objects.bulk_create([
            BookRent(
                user=User.objects.order_by('?').last(),
                book=Book.objects.order_by('?').last(),
                status=random.choice([ch[0] for ch in choices.BOOK_STATUSES])
            ) for _ in range(10_000)
        ])
        RentDayHistory.objects.bulk_create([
            RentDayHistory(rent=BookRent.objects.order_by('?').last())
            for _ in range(10_000)
        ])
