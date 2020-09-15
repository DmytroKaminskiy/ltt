from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic import RedirectView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions


API_PREFIX = 'api/v1/'

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('register/', RedirectView.as_view(url=reverse_lazy('account:django_registration_register'))),

    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('django_registration.backends.activation.urls')),

    path('', include('pages.urls')),
    path('account/', include('account.urls')),
    path('book/', include('book.urls')),

    path(f'{API_PREFIX}account/', include('account.api.urls')),
    path(f'{API_PREFIX}book/', include('book.api.urls')),

    re_path(fr'^{API_PREFIX}swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'{API_PREFIX}swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'{API_PREFIX}redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]
