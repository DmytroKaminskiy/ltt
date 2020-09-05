from account.models import User

from django.contrib.auth.hashers import make_password

import factory


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    password = factory.LazyFunction(lambda: make_password('password'))
    email = factory.Sequence(lambda n: f'person{n}@example.com')
