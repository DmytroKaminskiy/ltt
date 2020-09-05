from urllib.parse import urlparse

from account.models import User

from django.conf import settings
from django.core import mail
from django.urls import reverse, reverse_lazy

from tests.const import URLS_PATTERN

URL = reverse_lazy('account:django_registration_register')


def test_registration_get(client):
    response = client.get(URL)
    assert response.status_code == 200
    assert 'form' in response.context_data


def test_registration_create_empty_data(client):
    user_count = User.objects.count()
    response = client.post(URL, data={})
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'email': ['This field is required.'],
        'password1': ['This field is required.'],
        'password2': ['This field is required.'],
    }
    assert len(mail.outbox) == 0
    assert User.objects.count() == user_count


def test_registration_create_different_password(client, fake):
    user_count = User.objects.count()
    data = {
        'email': fake.email(),
        'password1': fake.password(),
        'password2': fake.password(),
    }
    response = client.post(URL, data=data)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'password2': ["The two password fields didn't match."]
    }
    assert len(mail.outbox) == 0
    assert User.objects.count() == user_count


def test_registration_create_same_password(client, fake):
    user_count = User.objects.count()
    data = {
        'email': fake.email(),
        'password1': fake.password(),
    }
    data['password2'] = data['password1']

    response = client.post(URL, data=data)
    assert response.status_code == 302
    assert response['Location'] == reverse('django_registration_complete')

    assert User.objects.count() == user_count + 1

    user = User.objects.last()
    assert user.email == data['email']
    assert user.is_active is False

    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == [data['email']]
    assert email.cc == []
    assert email.bcc == []
    assert email.reply_to == []
    assert email.from_email == settings.DEFAULT_FROM_EMAIL
    assert email.subject == 'Activate your Account'
    assert 'Thanks for signing up!' in email.body

    url = urlparse(URLS_PATTERN.findall(email.body)[-1])
    response = client.get(url.path)
    assert response.status_code == 302
    assert response['Location'] == reverse('django_registration_activation_complete')

    user.refresh_from_db()
    assert user.is_active is True

    # post same data again
    response = client.post(URL, data=data)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'email': ['This email address is already in use. Please supply a different email address.'],
    }

    assert User.objects.count() == user_count + 1
    assert len(mail.outbox) == 1

    assert response.wsgi_request.user.is_authenticated is False
    # test login wrong password
    response = client.post(
        reverse('login'),
        data={'username': data['email'], 'password': 'wrong-password'},
    )
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        '__all__': ['Please enter a correct email address and password. Note that both fields may be case-sensitive.']
    }
    assert response.wsgi_request.user.is_authenticated is False

    # test login wrong email
    response = client.post(
        reverse('login'),
        data={'username': fake.email(), 'password': data['password1']},
    )
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        '__all__': ['Please enter a correct email address and password. Note that both fields may be case-sensitive.']
    }
    assert response.wsgi_request.user.is_authenticated is False

    # test login correct
    assert response.wsgi_request.user.is_authenticated is False
    response = client.post(
        reverse('login'),
        data={'username': data['email'], 'password': data['password1']},
    )
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated is True
