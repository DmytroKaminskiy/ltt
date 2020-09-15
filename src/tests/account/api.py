from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories import UserFactory


def test_account_create(api_client, fake):
    url = reverse('account-api:users')
    data = {
        'email': fake.email(),
        'password': fake.password(),
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    r_json = response.json()
    assert r_json['access']
    assert r_json['id']
    assert r_json['email'] == data['email']

    # send same data, we should get an error where user was already created
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    r_json = response.json()
    assert len(r_json) == 1
    assert r_json['email'] == ['user with this email address already exists.']


def test_obtain_token(api_client):
    url = reverse('account-api:token_obtain')
    user = UserFactory()
    payload = {
        'email': user.email,
        'password': 'password',
    }
    response = api_client.post(url, data=payload)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()['access']
