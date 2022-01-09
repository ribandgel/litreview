from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views import View

from litreview.base.forms import LoginForm, SignUpForm, TicketForm
from litreview.base.models import UserFollow, Ticket, Review


class FluxView(View):
    template_name = "flux.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("home")
        tickets = Ticket.objects.all().order_by('-time_created')
        reviews = Review.objects.all().order_by('-time_created')
        return render(request, self.template_name, {'tickets': tickets, 'reviews': reviews, 'username': request.user.username})

class CreateTicketView(CreateView):
    model = Ticket
    template_name = "create_ticket.html"
    form_class = TicketForm
    success_url = "/flux/"

    def form_valid(self, form):
        breakpoint()
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        ticket.save()
        return super(CreateTicketView, self).form_valid(form)       


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
