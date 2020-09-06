from unittest import mock

from book import choices
from book.models import BookRent, Category, RentDayHistory
from book.tasks import history_update

from dateutil.relativedelta import relativedelta

from django.db.models import Sum
from django.utils import timezone

from tests.factories import BookFactory, UserFactory


def test_history_update(django_assert_num_queries):
    # prepare
    user = UserFactory()
    category_regular = Category.objects.get(name='regular')
    book_regular = BookFactory(category=category_regular)
    BookRent.objects.all().delete()

    in_use = [
        BookRent.objects.create(
            user=user,
            book_id=book_regular.id,
            status=choices.BOOK_STATUS_IN_USE,
        )
        for _ in range(3)
    ]
    [
        BookRent.objects.create(
            user=user,
            book_id=book_regular.id,
            status=choices.BOOK_STATUS_END,
        )
        for _ in range(5)
    ]

    count_history = RentDayHistory.objects.count()

    # should be updated only with status in use
    with django_assert_num_queries(5):
        history_update()
    assert RentDayHistory.objects.count() == count_history + len(in_use)

    for br in in_use:
        assert br.rentdayhistory_set.aggregate(total=Sum('amount'))['total'] == 1

    # should be the same after next call within same day
    history_update()
    assert RentDayHistory.objects.count() == count_history + 3
    for br in in_use:
        assert br.rentdayhistory_set.aggregate(total=Sum('amount'))['total'] == 1

    # let's try for tomorrow
    tomorrow = timezone.now() + relativedelta(days=1)
    with mock.patch.object(timezone, 'now', return_value=tomorrow):
        # should be updated only with status in use
        with django_assert_num_queries(5):
            history_update()
        assert RentDayHistory.objects.count() == count_history + len(in_use) * 2

        for br in in_use:
            assert br.rentdayhistory_set.aggregate(total=Sum('amount'))['total'] == 2

    # and after tomorrow
    after_tomorrow = timezone.now() + relativedelta(days=2)
    with mock.patch.object(timezone, 'now', return_value=after_tomorrow):
        # should be updated only with status in use
        with django_assert_num_queries(5):
            history_update()
        assert RentDayHistory.objects.count() == count_history + len(in_use) * 3

        for br in in_use:
            assert br.rentdayhistory_set.aggregate(total=Sum('amount'))['total'] == 3.5

    # and after-after tomorrow)))
    future = timezone.now() + relativedelta(days=3)
    with mock.patch.object(timezone, 'now', return_value=future):
        # should be updated only with status in use
        with django_assert_num_queries(5):
            history_update()
        assert RentDayHistory.objects.count() == count_history + len(in_use) * 4

        for br in in_use:
            assert br.rentdayhistory_set.aggregate(total=Sum('amount'))['total'] == 5

    # finalize
    BookRent.objects.update(status=choices.BOOK_STATUS_END)
    future = timezone.now() + relativedelta(days=4)
    with mock.patch.object(timezone, 'now', return_value=future):
        # should be updated only with status in use
        with django_assert_num_queries(1):
            history_update()
        assert RentDayHistory.objects.count() == count_history + len(in_use) * 4

        for br in in_use:
            assert br.rentdayhistory_set.aggregate(total=Sum('amount'))['total'] == 5
