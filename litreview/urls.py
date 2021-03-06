"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from litreview.base.views import (
    CreateReviewToTicketView,
    CreateReviewView,
    CreateSubscriptionView,
    CreateTicketView,
    DeleteSubscriptionView,
    FluxView,
    HomeView,
    PostView,
    ReviewDeleteView,
    ReviewUpdateView,
    SignUpView,
    SubscriptionsView,
    TicketDeleteView,
    TicketUpdateView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", HomeView.as_view(), name="home"),
    path("flux/", FluxView.as_view(), name="flux"),
    path("posts/", PostView.as_view(), name="posts"),
    path("subscriptions/", SubscriptionsView.as_view(), name="subscriptions"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("follow/", CreateSubscriptionView.as_view(), name="follow"),
    path("unfollow/<int:pk>/", DeleteSubscriptionView.as_view(), name="unfollow"),
    path("tickets/create_ticket", CreateTicketView.as_view(), name="create_ticket"),
    path("tickets/<int:pk>/update_ticket", TicketUpdateView.as_view(), name="update_ticket"),
    path("tickets/<int:pk>/delete_ticket", TicketDeleteView.as_view(), name="delete_ticket"),
    path("reviews/create_review", CreateReviewView.as_view(), name="create_review"),
    path("tickets/<int:pk>/update_review", ReviewUpdateView.as_view(), name="update_review"),
    path("tickets/<int:pk>/delete_review", ReviewDeleteView.as_view(), name="delete_review"),
    path(
        "reviews/<int:pk>/create_review_to_ticket",
        CreateReviewToTicketView.as_view(),
        name="create_review_to_ticket",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
