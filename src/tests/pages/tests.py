from django.urls import reverse


def test_index(client):
    url = reverse('pages:index')
    response = client.get(url)
    assert response.status_code == 200


def test_index_redirect(client_auth):
    url = reverse('pages:index')
    response = client_auth.get(url)
    assert response.status_code == 302
    assert response['Location'] == reverse('book:book-list')
