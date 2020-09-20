from book import views

from django.urls import path


app_name = 'book'

urlpatterns = [
    path('rent-book/create/', views.CreateBookRentView.as_view(), name='rent-create'),
    path('book/list/', views.BookList.as_view(), name='book-list'),
    path('search/', views.SearchBook.as_view(), name='search'),
    path('rents-billing/', views.BookRentTableBillingView.as_view(), name='rents'),
    path('rents-table/', views.BookRentTableView.as_view(), name='rents-table'),
]
