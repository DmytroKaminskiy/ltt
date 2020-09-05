from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('book:rent-create')

        return super().dispatch(request, *args, **kwargs)
