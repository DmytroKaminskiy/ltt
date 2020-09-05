from book import choices
from book.models import Book, BookRent

from django.urls import reverse, reverse_lazy


URL = reverse_lazy('book:rent-create')


def test_create_rate_get(client_auth):
    response = client_auth.get(URL)
    assert response.status_code == 200


def test_create_rate_post_empty_data(client_auth):
    count_book_rent = BookRent.objects.count()
    response = client_auth.post(URL, data={})
    assert response.status_code == 200

    assert response.context_data['form'].errors == {
        'book': ['This field is required.'],
    }
    assert BookRent.objects.count() == count_book_rent


def test_create_rate_post_wrong_id(client_auth):
    count_book_rent = BookRent.objects.count()
    payload = {
        'book': 9999999,
    }

    response = client_auth.post(URL, data=payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'book': ['Select a valid choice. That choice is not one of the available choices.']
    }
    assert BookRent.objects.count() == count_book_rent


def test_create_rate_post(client_auth):
    count_book_rent = BookRent.objects.count()
    payload = {
        'book': Book.objects.last().id,
    }

    response = client_auth.post(URL, data=payload)
    assert response.status_code == 302
    assert response['Location'] == reverse('account:profile_overall')
    assert BookRent.objects.count() == count_book_rent + 1


def test_search(client_auth):
    url = reverse('book:search')
    response = client_auth.get(url)
    assert response.status_code == 200
    assert response.json() == []

    response = client_auth.get(url + '?search=career')
    assert response.status_code == 200
    assert response.json()


def test_bookrenttable(client_auth):
    # prepare
    user = client_auth.user
    book = Book.objects.last()
    book_rent = BookRent.objects.create(user=user, book=book, status=choices.BOOK_STATUS_CONFIRMED)
    book_rent.status = choices.BOOK_STATUS_IN_USE
    book_rent.save()
    assert book_rent.rentdayhistory_set.count() == 1

    url = reverse('book:rents')
    response = client_auth.get(url)
    assert response.status_code == 200
