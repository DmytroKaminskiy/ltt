import os
from urllib.parse import urlparse

from account.models import User

from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.urls import reverse

from faker import Faker

import pytest

from pytest_django.fixtures import _django_db_fixture_helper

from pytest_factoryboy import register

from rest_framework.test import APIClient

from tests.const import PASSWORD, URLS_PATTERN
from tests.factories import *  # noqa


register(UserFactory)  # noqa
register(BookFactory)  # noqa


@pytest.fixture(scope='session', autouse=True)
def db_session(request, django_db_setup, django_db_blocker):
    """
    Changed scope to 'session'
    """
    if 'django_db_reset_sequences' in request.funcargnames:
        request.getfixturevalue('django_db_reset_sequences')
    if 'transactional_db' in request.funcargnames \
            or 'live_server' in request.funcargnames:
        request.getfixturevalue('transactional_db')
    else:
        _django_db_fixture_helper(request, django_db_blocker, transactional=False)


@pytest.fixture(scope='session', autouse=True)
def fixtures():
    for fixture in ('category', 'book'):
        call_command('loaddata', os.path.join(settings.BASE_DIR, 'tests', 'fixtures', f'{fixture}.json'))


@pytest.fixture(scope="session")
def fake():
    yield Faker()


@pytest.fixture(scope='function')
def client_auth(client, fake):
    user_count = User.objects.count()
    url = reverse('account:django_registration_register')

    data = {
        'email': fake.email(),
        'password1': PASSWORD,
        'password2': PASSWORD,
    }

    response = client.post(url, data=data)
    assert response.status_code == 302
    assert User.objects.count() == user_count + 1
    assert len(mail.outbox) == 1
    email = mail.outbox[-1]

    activate_url = urlparse(URLS_PATTERN.findall(email.body)[-1])
    response = client.get(activate_url.path)
    assert response.status_code == 302

    # test login correct
    # assert response.wsgi_request.user.is_active is True
    assert response.wsgi_request.user.is_authenticated is False
    response = client.post(
        reverse('login'),
        data={'username': data['email'], 'password': data['password1']},
    )
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated is True
    client.user = response.wsgi_request.user

    yield client


@pytest.fixture(scope='session')
def api_client():
    yield APIClient()
