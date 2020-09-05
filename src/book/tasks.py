from book import choices

from django.utils import timezone

from settings import celery_app as app


@app.task(time_limit=60 * 60 * 2)  # set hard limit 2 hours
def history_update():
    from book.models import BookRent, RentDayHistory

    today = timezone.now().date()

    filter_kwargs = {
        'status': choices.BOOK_STATUS_IN_USE,
        'created': today,
    }
    exclude_kwargs = {
        'rentdayhistory__created': today,
    }

    rents = []
    queryset = BookRent.objects\
        .filter(**filter_kwargs)\
        .exclude(**exclude_kwargs)\
        .only('id', 'price')\
        .iterator()

    for book_rent in queryset:
        rents.append(RentDayHistory(rent_id=book_rent.id, amount=book_rent.price))

        # create new rent day by chunks
        if len(rents) == 10_000:
            RentDayHistory.objects.bulk_create(rents)
            rents.clear()
    else:
        # create rent history if loop was ended and len(rents) wasn't 10_000
        RentDayHistory.objects.bulk_create(rents)
        rents.clear()
