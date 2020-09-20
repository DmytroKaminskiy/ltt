from book.api.serializers.bookrent import BookRentSerializer
from book.models import BookRent

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from rest_framework_simplejwt.authentication import JWTAuthentication


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
    authentication_classes = (SessionAuthentication, JWTAuthentication)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveBookRentView(BaseView, generics.RetrieveAPIView):
    pass
