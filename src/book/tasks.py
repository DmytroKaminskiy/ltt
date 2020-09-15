from book import choices

from django.db.models import F
from django.utils import timezone

from settings import celery_app as app


@app.task(time_limit=60 * 60 * 2)  # set hard limit 2 hours
def history_update():
    from book.models import BookRent, RentDayHistory

    today = timezone.now().date()
    rents = []

    queryset = BookRent.objects\
        .filter(status=choices.BOOK_STATUS_IN_USE)\
        .exclude(rentdayhistory__created=today)\
        .only('id', 'price', 'days_period', 'price_period')

    book_rent_queryset = BookRent.objects.exclude(days_period=0)
    days_period_f = F('days_period') - 1

    book_rent_ids = set()

    for book_rent in queryset.iterator():
        rents.append(RentDayHistory(
            rent_id=book_rent.id,
            amount=book_rent.get_price())
        )
        book_rent_ids.add(book_rent.id)

        # create new rent day by chunks
        if len(rents) == 10_000:
            RentDayHistory.objects.bulk_create(rents)
            book_rent_queryset.filter(id__in=book_rent_ids).update(days_period=days_period_f)
            book_rent_ids.clear()
            rents.clear()
    else:
        # create rent history if loop was ended and len(rents) wasn't 10_000
        RentDayHistory.objects.bulk_create(rents)
        book_rent_queryset.filter(id__in=book_rent_ids).update(days_period=days_period_f)
        book_rent_ids.clear()
        rents.clear()
