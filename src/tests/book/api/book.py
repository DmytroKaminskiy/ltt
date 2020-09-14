from book.models import Book, Category

from rest_framework.reverse import reverse


def test_book_create_empty_data(api_client_auth):
    count_books = Book.objects.count()
    url = reverse('book-api:books')

    response = api_client_auth.post(url, data={}, format='json')
    assert response.status_code == 400
    assert response.json() == {
        'title': ['This field is required.'],
        'category': ['This field is required.'],
    }
    assert Book.objects.count() == count_books


def test_books(api_client_auth):
    count_categories = Book.objects.count()
    url = reverse('book-api:books')
    category = Category.objects.last()

    data = {
        'title': 'Test Title Data',
        'category': category.id,
    }

    # test create
    response = api_client_auth.post(url, data=data, format='json')
    assert response.status_code == 201
    assert Book.objects.count() == count_categories + 1
    book = Book.objects.last()
    assert response.json() == {
        'id': book.id,
        'category': category.id,
        'title': 'Test Title Data',
    }

    # test get list
    response = api_client_auth.get(url)
    assert response.status_code == 200
    assert response.json()

    # test retrieve one object
    url = reverse('book-api:book', args=(book.id,))
    response = api_client_auth.get(url)
    assert response.json() == {
        'id': book.id,
        'category': category.id,
        'title': 'Test Title Data',
    }
