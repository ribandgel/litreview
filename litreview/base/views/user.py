from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from litreview.base.forms import LoginForm, SignUpForm
from litreview.base.models import UserFollow


class FluxView(TemplateView):
    template_name = "flux.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("home")
        return super().get(self, request)


class HomeView(LoginView):
    template_name = "home.html"
    form_class = LoginForm
    success_url = "/flux/"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("flux")
        return super().get(self, request)


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = "/flux/"

class PostsView(ListView):
    template_name = "posts.html"
