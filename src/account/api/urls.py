from account.api import views

from django.urls import path


app_name = 'account-api'

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('token/', views.TokenObtainView.as_view(), name='token_obtain'),
]
