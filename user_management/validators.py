# user_management/validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class StrongPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        print(f"Validating password: {password}")  # Add this line for debugging

        if len(password) < self.min_length:
            raise ValidationError(
                _("Password must be at least %(min_length)d characters long."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

        # Add additional strength checks here if needed

    def get_help_text(self):
        return _(
            "Your password must be at least %(min_length)d characters long."
        ) % {'min_length': self.min_length}
