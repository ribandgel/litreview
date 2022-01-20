from django.contrib.auth.views import LoginView
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from litreview.base.forms import LoginForm, SignUpForm, TicketForm
from litreview.base.models import Review, Ticket


class FluxView(View):
    template_name = "flux.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("home")
        tickets = Ticket.objects.all().order_by("-time_created")
        reviews = Review.objects.all().order_by("-time_created")
        return render(
            request,
            self.template_name,
            {"tickets": tickets, "reviews": reviews, "username": request.user.username},
        )


class CreateTicketView(CreateView):
    model = Ticket
    template_name = "create_ticket.html"
    form_class = TicketForm
    success_url = "/flux/"

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        ticket.save()
        return super(CreateTicketView, self).form_valid(form)


class CreateReviewView(CreateView):
    template_name = "create_review.html"
    success_url = "/flux/"
    model = Ticket
    fields = ("title", "description", "image")
    exclude = "user"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            redirect("home")
        ReviewFormSet = inlineformset_factory(
            Ticket, Review, fields=("headline", "body", "rating"), exclude=("user",), max_num=1
        )
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["review"] = ReviewFormSet(self.request.POST)
        else:
            data["review"] = ReviewFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        review_form = context["review"]
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        ticket.save()
        if review_form.is_valid():
            review_form.instance = ticket
            reviews = review_form.save(commit=False)
            review = reviews[0]
            review.user = ticket.user
            review.save()
        return super().form_valid(form)


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
