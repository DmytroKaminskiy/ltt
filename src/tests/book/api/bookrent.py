from book.models import Book, BookRent

from rest_framework.reverse import reverse


def test_book_rent_create_empty_data(api_client_auth):
    count_book_rents = BookRent.objects.count()
    url = reverse('book-api:book-rents')

    response = api_client_auth.post(url, data={}, format='json')
    assert response.status_code == 400
    assert response.json() == {'book': ['This field is required.']}
    assert BookRent.objects.count() == count_book_rents


def test_book_rents(api_client_auth):
    count_book_rents = BookRent.objects.count()
    url = reverse('book-api:book-rents')
    book = Book.objects.last()

    data = {
        'book': book.id,
    }

    # test create
    response = api_client_auth.post(url, data=data, format='json')
    assert response.status_code == 201
    assert BookRent.objects.count() == count_book_rents + 1
    book_rent = BookRent.objects.last()

    assert response.json() == {
        'created': str(book_rent.created),
        'days_period': 2,
        'days_period_initial': 2,
        'end': None,
        'id': book_rent.id,
        'book': book.id,
        'price': '1.50',
        'price_period': '4.50',
        'status': 1,
        'user_id': response.wsgi_request.user.id
    }

    # test get list
    response = api_client_auth.get(url)
    assert response.status_code == 200
    assert response.json()

    # test retrieve one object
    url = reverse('book-api:book-rent', args=(book_rent.id,))
    response = api_client_auth.get(url)
    assert response.json() == {
        'created': str(book_rent.created),
        'days_period': 2,
        'days_period_initial': 2,
        'end': None,
        'id': book_rent.id,
        'book': book.id,
        'price': '1.50',
        'price_period': '4.50',
        'status': 1,
        'user_id': response.wsgi_request.user.id
    }
