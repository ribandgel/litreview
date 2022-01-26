from django.contrib.auth.views import LoginView
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from litreview.base.forms import LoginForm, SignUpForm, TicketForm, ReviewForm
from litreview.base.models import Review, Ticket


class FluxView(LoginRequiredMixin, View):
    template_name = "flux.html"
    login_url = reverse_lazy("home")

    def get(self, request):
        tickets = Ticket.objects.all().order_by("-time_created")
        reviews = Review.objects.all().order_by("-time_created")
        return render(
            request,
            self.template_name,
            {"tickets": tickets, "reviews": reviews, "username": request.user.username},
        )

class PostView(LoginRequiredMixin, View):
    template_name = "posts.html"
    login_url = reverse_lazy("home")

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
        reviews = Review.objects.filter(user=request.user).order_by("-time_created")
        return render(
            request,
            self.template_name,
            {"tickets": tickets, "reviews": reviews, "username": request.user.username},
        )


class CreateTicketView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = "create_ticket.html"
    form_class = TicketForm
    success_url = reverse_lazy("flux")
    login_url = reverse_lazy("home")

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        ticket.save()
        return super(CreateTicketView, self).form_valid(form)

class CreateReviewToTicketView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = "create_review_to_ticket.html"
    form_class = ReviewForm
    success_url = reverse_lazy("flux")
    login_url = reverse_lazy("home")

    def form_valid(self, form):
        breakpoint()
        review = form.save(commit=False)
        review.user = self.request.user
        pk = self.request.resolver_match.kwargs.pop("pk")
        try:
            review.ticket = Ticket.objects.get(id=pk)
        except Ticket.DoesNotExist:
            return reverse_lazy("flux")
        review.save()
        return super(CreateReviewToTicketView, self).form_valid(form)

    def get(self, request, pk):
        try:
            ticket = Ticket.objects.get(id=pk)
        except Ticket.DoesNotExist:
            return reverse_lazy("flux")
        return render(
            request,
            self.template_name,
            {"ticket": ticket, "form": self.get_form()},
        )


class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = "create_review.html"
    success_url = "/flux/"
    model = Ticket
    fields = ("title", "description", "image")
    exclude = "user"
    login_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
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

