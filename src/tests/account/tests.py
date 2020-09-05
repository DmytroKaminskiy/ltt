from django.urls import reverse


def test_profile_overall(client_auth):
    url = reverse('account:profile_overall')
    response = client_auth.get(url)
    assert response.status_code == 200
