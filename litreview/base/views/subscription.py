from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from litreview.base.forms import SubscriptionForm
from litreview.base.models import User, UserFollow


class SubscriptionsView(LoginRequiredMixin, ListView):
    template_name = "subscriptions.html"
    model = UserFollow

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscribers"] = self.request.user.followed_by.all()
        context["subscriptions"] = self.request.user.following.all()
        return context

class CreateSubscriptionView(LoginRequiredMixin, FormView):
    model = UserFollow
    fields = ["followed_user"]
    success_url = "/subscriptions/"
    template_name = "subscriptions.html"
    form_class = SubscriptionForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            following_user_name = form.cleaned_data.get("followed_user")
            try:
                target = User.objects.get(username=following_user_name)
            except User.DoesNotExist:
                pass
            else:
                if request.user != target:
                    try:
                        UserFollow.objects.create(user=request.user, followed_user=target)
                    except Exception:
                        pass

        return redirect(self.success_url)


class DeleteSubscriptionView(LoginRequiredMixin, DeleteView):
    model = UserFollow
    template_name = "subscriptions.html"
    success_url = "/subscriptions/"
    login_url = reverse_lazy("home")
