# from django.views.decorators.cache import cache_page
from django.urls import path

from pages import views

app_name = 'pages'

urlpatterns = [
    path(
        '',
        # TODO cache_page(60*60*2)(views.IndexView.as_view()),
        views.IndexView.as_view(),
        name='index',
    ),
]
