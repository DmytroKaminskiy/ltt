from book.models import Book

import factory


class BookFactory(factory.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence')
