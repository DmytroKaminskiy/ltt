from book.models import Category

from rest_framework.reverse import reverse


def test_category_create_empty_data(api_client_auth):
    count_categories = Category.objects.count()
    url = reverse('book-api:categories')

    response = api_client_auth.post(url, data={}, format='json')
    assert response.status_code == 400
    assert response.json() == {'name': ['This field is required.'], 'price': ['This field is required.']}
    assert Category.objects.count() == count_categories


def test_category(api_client_auth):
    count_categories = Category.objects.count()
    url = reverse('book-api:categories')
    data = {'name': 'Test Title Data', 'price': '1'}

    # test create
    response = api_client_auth.post(url, data=data, format='json')
    assert response.status_code == 201
    assert Category.objects.count() == count_categories + 1
    category = Category.objects.last()
    assert response.json() == {
        'id': category.id,
        'days_period': 0,
        'name': 'Test Title Data',
        'price': '1.00',
        'price_period': '0.00',
    }

    # test get list
    response = api_client_auth.get(url)
    assert response.status_code == 200
    assert response.json()

    # test retrieve one object
    url = reverse('book-api:category', args=(category.id, ))
    response = api_client_auth.get(url)
    assert response.json() == {
        'id': category.id,
        'days_period': 0,
        'name': 'Test Title Data',
        'price': '1.00',
        'price_period': '0.00',
    }
