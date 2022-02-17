from django.contrib.auth.views import LoginView
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, Value
from itertools import chain

from litreview.base.forms import LoginForm, SignUpForm, TicketForm, ReviewForm, ReviewFormSet
from litreview.base.models import Review, Ticket


class FluxView(LoginRequiredMixin, TemplateView):
    template_name = "flux.html"
    login_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        tickets = Ticket.objects.filter(user__in=self.request.user.following.all().values("followed_user")).annotate(content_type=Value("TICKET", CharField()))
        reviews = Review.objects.filter(user__in=self.request.user.following.all().values("followed_user")).annotate(content_type=Value("REVIEW", CharField()))
        context = super().get_context_data(**kwargs)
        posts = sorted(chain(tickets, reviews), key= lambda post: post.time_created, reverse=True)
        context["posts"] = posts
        context["username"] = self.request.user.username
        return context

class PostView(LoginRequiredMixin, TemplateView):
    template_name = "posts.html"
    login_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        tickets = Ticket.objects.filter(user=self.request.user).annotate(content_type=Value("TICKET", CharField()))
        reviews = Review.objects.filter(user=self.request.user).annotate(content_type=Value("REVIEW", CharField()))
        context = super().get_context_data(**kwargs)
        posts = sorted(chain(tickets, reviews), key= lambda post: post.time_created, reverse=True)
        context["posts"] = posts
        context["username"] = self.request.user.username
        return context

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

    def get_context_data(self, **kwargs):
        ticket = get_object_or_404(Ticket, id=self.kwargs.get("pk"))
        context = super().get_context_data(**kwargs)
        context["ticket"] = ticket
        return context
        '''     return render(
                     request,
                     self.template_name,
                     {"ticket": ticket, "form": self.get_form()},
                 )
        '''

class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = "create_review.html"
    success_url = "/flux/"
    form_class = TicketForm
    login_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        ReviewForm = inlineformset_factory(
            Ticket, Review, fields=("headline", "body", "rating"), exclude=("user",), max_num=1, formset=ReviewFormSet
        )
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["review"] = ReviewForm(self.request.POST)
        else:
            data["review"] = ReviewForm()
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

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "update_review.html"

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "update_ticket.html"

class HomeView(LoginView):
    template_name = "home.html"
    form_class = LoginForm
    success_url = "/flux/"

class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = "/flux/"

