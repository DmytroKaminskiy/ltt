from book.api.serializers.book import BookSerializer
from book.models import Book

from rest_framework import generics


__all__ = [
    'ListCreateBookView',
    'RetrieveBookView',
]


class ListCreateBookView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('-id')


class RetrieveBookView(generics.RetrieveAPIView):
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
