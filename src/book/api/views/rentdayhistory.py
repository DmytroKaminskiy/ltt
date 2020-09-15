from book.api.serializers.bookrenthistory import RentDayHistorySerializer
from book.models import RentDayHistory

from rest_framework import generics


__all__ = [
    'ListBookRentHistoryView',
    'RetrieveBookRentHistoryView',
]


class BaseView:
    serializer_class = RentDayHistorySerializer
    queryset = RentDayHistory.objects.all().order_by('-id')

    def get_queryset(self):
        return super().get_queryset().filter(rent__user_id=self.request.user.id)


class ListBookRentHistoryView(BaseView, generics.ListAPIView):
    pass


class RetrieveBookRentHistoryView(BaseView, generics.RetrieveAPIView):
    pass
