from book import views

from django.urls import path


app_name = 'book'

urlpatterns = [
    path('rent-book/create/', views.CreateBookRentView.as_view(), name='rent-create'),
    path('search/', views.SearchBook.as_view(), name='search'),
    path('rents/', views.BookRentTable.as_view(), name='rents'),
]
