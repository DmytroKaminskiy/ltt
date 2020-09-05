from django.urls import reverse


def test_index(client):
    url = reverse('pages:index')
    response = client.get(url)
    assert response.status_code == 200
