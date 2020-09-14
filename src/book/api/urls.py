from book.api import views

from django.urls import path

app_name = 'book-api'


urlpatterns = [
    # book
    path('b/', views.ListCreateBookView.as_view(), name='books'),
    path('b/<int:pk>/', views.RetrieveBookView.as_view(), name='book'),

    # category
    path('categories/', views.ListCreateCategoryView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.RetrieveCategoryView.as_view(), name='category'),

    # book rent
    path('book-rents/', views.ListCreateBookRentView.as_view(), name='book-rents'),
    path('book-rents/<int:pk>/', views.RetrieveBookRentView.as_view(), name='book-rent'),

    # book rent history
    path('book-rents-history/', views.ListBookRentHistoryView.as_view(), name='book-rents-history'),
    path('book-rents-history/<int:pk>/', views.RetrieveBookRentHistoryView.as_view(), name='book-rent-history'),
]
