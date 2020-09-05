import random

from book import choices
from book.models import Book, BookRent, RentDayHistory
from book.tasks import history_update

from tests.factories import UserFactory


def test_history_update():
    # prepare
    user = UserFactory()
    books = list(Book.objects.values_list('id', flat=True))

    in_use = [
        BookRent(
            user=user,
            book_id=random.choice(books),
            status=choices.BOOK_STATUS_IN_USE)
        for _ in range(3)
    ]
    end = [
        BookRent(
            user=user,
            book_id=random.choice(books),
            status=choices.BOOK_STATUS_END)
        for _ in range(5)
    ]
    BookRent.objects.bulk_create(in_use + end)

    count_history = RentDayHistory.objects.count()

    # should be updated only with status in use
    history_update()
    assert RentDayHistory.objects.count() == count_history + 3

    # should be the same after next call within same day
    history_update()
    assert RentDayHistory.objects.count() == count_history + 3
