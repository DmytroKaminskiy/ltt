from urllib.parse import urlencode

from book.filters import BookFilter
from book.forms import BookRentForm
from book.models import Book, BookRent, RentDayHistory

from decorators import lock_for_user

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, CharField, Count, F, Sum, Value, When
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, View

from django_filters.views import FilterView

__all__ = [
    'CreateBookRentView', 'SearchBook', 'BookRentTableBillingView',
    'BookRentTableView', 'BookList',
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
        data = list(self.get_queryset())
        return JsonResponse(data, safe=False)

    def get_queryset(self):
        # generate human readable tariff and category name
        case = Case(
            When(
                category__days_period=0,
                then=Concat(
                    Value('Title: '),
                    F('title'),
                    Value(' $'),
                    F('category__price'),
                    Value(' each day. Category: '),
                    F('category__name'),
                )
            ),
            default=Concat(
                Value('Title: '),
                F('title'),
                Value(' $'),
                F('category__price_period'),
                Value(' for first '),
                F('category__days_period'),
                Value(' day/s. $'),
                F('category__price'),
                Value(' each day afterwards. Category: '),
                F('category__name'),
            ),
            output_field=CharField(),
        )
        values = ('id', 'title', 'price_display', 'category__name')
        limit = 10

        return Book.objects \
            .filter(title__search=self.search_term) \
            .annotate(price_display=case) \
            .values(*values)[:limit]

    @property
    def search_term(self):
        return self.request.GET.get('search') or ''


class BookRentTableBillingView(LoginRequiredMixin, ListView):
    queryset = RentDayHistory.objects.all()
    template_name = 'account/rent_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        values = (
            'rent_id', 'rent', 'rent__book__title',
            'rent__status', 'rent__end', 'rent__book__category__name'
        )
        # generate human readable tariff
        tariff = Case(
            When(
                rent__days_period_initial=0,
                then=Concat(
                    Value('$'),
                    F('rent__price'),
                    Value(' each day.'),
                )
            ),
            default=Concat(
                Value('$'),
                F('rent__price_period'),
                Value(' for first '),
                F('rent__days_period_initial'),
                Value(' day/s. $'),
                F('rent__price'),
                Value(' each day afterwards.'),
            ),
            output_field=CharField(),
        )
        return queryset\
            .filter(rent__user_id=self.request.user.id)\
            .values(*values)\
            .annotate(
                total_amount=Sum('amount'),
                count=Count('id'),
                tariff=tariff,
            )


class BookRentTableView(LoginRequiredMixin, ListView):
    queryset = BookRent.objects.all().select_related('book')
    template_name = 'account/rent_list_table.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # generate human readable tariff and category name
        tariff = Case(
            When(
                days_period_initial=0,
                then=Concat(
                    Value('$'),
                    F('price'),
                    Value(' each day.'),
                )
            ),
            default=Concat(
                Value('$'),
                F('price_period'),
                Value(' for first '),
                F('days_period_initial'),
                Value(' day/s. $'),
                F('price'),
                Value(' each day afterwards.'),
            ),
            output_field=CharField(),
        )
        return queryset.filter(user_id=self.request.user.id).annotate(tariff=tariff)


class BookList(FilterView):
    queryset = Book.objects.all().select_related('category').order_by('-id')
    template_name = 'account/book_list.html'
    paginate_by = 12
    filterset_class = BookFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        get = dict(tuple(self.request.GET.items()))
        get.pop('page', None)
        context['request_GET'] = urlencode(get)
        return context
