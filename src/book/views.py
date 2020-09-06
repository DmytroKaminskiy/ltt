from book.forms import BookRentForm
from book.models import Book, BookRent, RentDayHistory

from decorators import lock_for_user

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, View

__all__ = [
    'CreateBookRentView', 'SearchBook', 'BookRentTableBillingView',
    'BookRentTableView',
]


class CreateBookRentView(LoginRequiredMixin, CreateView):
    model = BookRent
    template_name = 'account/rent_create.html'
    form_class = BookRentForm
    success_url = reverse_lazy('account:profile_overall')

    @method_decorator(lock_for_user(methods=('POST',)))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Book Rent was created successfully.')
        return super().get_success_url()


class SearchBook(LoginRequiredMixin, View):
    def get(self, request):
        # wrap in list(), because QuerySet is not JSON serializable
        search_term = request.GET.get('search') or ''
        data = list(Book.objects.filter(title__search=search_term).values('id', 'title')[:10])
        return JsonResponse(data, safe=False)


class BookRentTableBillingView(LoginRequiredMixin, ListView):
    queryset = RentDayHistory.objects.all()
    template_name = 'account/rent_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset\
            .filter(rent__user_id=self.request.user.id)\
            .values('rent_id', 'rent', 'rent__book__title', 'rent__status', 'rent__end')\
            .annotate(total_amount=Sum('amount'))


class BookRentTableView(LoginRequiredMixin, ListView):
    queryset = BookRent.objects.all().select_related('book')
    template_name = 'account/rent_list_table.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
