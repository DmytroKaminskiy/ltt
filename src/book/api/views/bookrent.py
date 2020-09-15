from book.api.serializers.bookrent import BookRentSerializer
from book.models import BookRent

from rest_framework import generics


__all__ = [
    'ListCreateBookRentView',
    'RetrieveBookRentView',
]


class BaseView:
    serializer_class = BookRentSerializer
    queryset = BookRent.objects.all().order_by('-id')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class ListCreateBookRentView(BaseView, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveBookRentView(BaseView, generics.RetrieveAPIView):
    pass
