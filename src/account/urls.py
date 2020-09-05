from account import views

from django.urls import path


app_name = 'account'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='django_registration_register'),
    path('profile/details/', views.ProfileOverall.as_view(), name='profile_overall'),
]
