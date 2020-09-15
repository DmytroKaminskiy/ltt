from rest_framework.reverse import reverse


def test_book_rent_history(api_client_auth):
    url = reverse('book-api:book-rents-history')

    # test get list
    response = api_client_auth.get(url)
    assert response.status_code == 200
    assert response.json()
