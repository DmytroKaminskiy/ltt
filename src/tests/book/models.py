from book import choices
from book.models import Book, BookRent

from tests.factories import UserFactory


def test_bookrent_status_change():
    user = UserFactory()
    book = Book.objects.last()

    book_rent = BookRent.objects.create(user=user, book=book)
    assert book_rent.rentdayhistory_set.count() == 0

    # change status to BOOK_STATUS_CONFIRMED
    book_rent.status = choices.BOOK_STATUS_CONFIRMED
    book_rent.save()
    assert book_rent.rentdayhistory_set.count() == 0

    # change status to BOOK_STATUS_IN_USE
    book_rent.status = choices.BOOK_STATUS_IN_USE
    book_rent.save()
    assert book_rent.rentdayhistory_set.count() == 1
    assert book_rent.end is None

    # change status to BOOK_STATUS_END
    book_rent.status = choices.BOOK_STATUS_END
    book_rent.save()
    assert book_rent.rentdayhistory_set.count() == 1
    assert book_rent.end is not None
