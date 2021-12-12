from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from litreview.base.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
