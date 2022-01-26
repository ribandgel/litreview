from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, BaseInlineFormSet
from litreview.base.models import Review, Ticket, User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ("headline", "body", "rating")
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ReviewFormSet(BaseInlineFormSet):
     def __init__(self, *args, **kwargs):
        super(ReviewFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            for visible in form.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

