from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from litreview.base.models import User, Ticket


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")
        exclude = ("user",)
