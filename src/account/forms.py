from account.models import User

from django_registration.forms import RegistrationForm, RegistrationFormUniqueEmail


__all__ = [
    'UserRegistrationForm',
]


class UserRegistrationForm(RegistrationFormUniqueEmail):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = [
            User.USERNAME_FIELD,
            # User.get_email_field_name(),
            "password1",
            "password2",
        ]
