import urllib.parse

from account.forms import UserRegistrationForm
from account.models import User

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView


from django_registration.backends.activation.views import RegistrationView as RV


__all__ = ['RegistrationView', 'ProfileOverall']

REGISTRATION_SALT = getattr(settings, "REGISTRATION_SALT", "registration")


class RegistrationView(RV):
    form_class = UserRegistrationForm
    email_body_template = "django_registration/activation_email_body"

    def get_email_context(self, *args, **kwargs):
        c = super().get_email_context(*args, **kwargs)
        path = reverse("django_registration_activate", args=(c['activation_key'],))
        domain = settings.DOMAIN
        c['activation_link'] = f'http://{domain}{path}'
        return c

    def get_success_url(self, user=None):
        if user:
            self.request.session['email'] = urllib.parse.quote(user.email)
        return super().get_success_url(user)

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.
        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context["user"] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request,
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = "".join(subject.splitlines())
        text_content = render_to_string(f'{self.email_body_template}.txt', context)
        html_content = render_to_string(f'{self.email_body_template}.html', context)

        user.email_user(subject, text_content, settings.DEFAULT_FROM_EMAIL, html_message=html_content)


class ProfileOverall(LoginRequiredMixin, DetailView):
    queryset = User.objects.all()

    def get_object(self, queryset=None):
        return self.request.user
