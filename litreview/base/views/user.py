from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from litreview.base.models import Ticket, Review

def signup(request):
    if request.user.is_authenticated:
        redirect("flux")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("flux")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def home(request):
    if request.user.is_authenticated:
        redirect("flux")
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("flux")
    else:
        form = AuthenticationForm()
    return render(request, "home.html", {"form": form})

def flux(request):
    if not request.user.is_authenticated:
        redirect("home")
    tickets = Ticket.objects.filter(user=request.user).order_by("time_created")
    reviews = Review.objects.filter(user=request.user).order_by("time_created")
    return render(request, "flux.html", {"tickets": tickets, "reviews": reviews})
