from book.models import Book

import django_filters


class BookFilter(django_filters.FilterSet):

    class Meta:
        model = Book
        fields = {
            'title': ['icontains', ]
        }
