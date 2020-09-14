from book.api.serializers.category import CategorySerializer
from book.models import Category

from rest_framework import generics


__all__ = [
    'ListCreateCategoryView',
    'RetrieveCategoryView',
]


class ListCreateCategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id')


class RetrieveCategoryView(generics.RetrieveAPIView):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
