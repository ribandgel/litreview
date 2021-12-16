from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView

from litreview.base.models import UserFollow, User
from litreview.base.forms import SubscriptionForm

class SubscriptionsView(ListView):
    template_name = 'subscriptions.html'
    model = UserFollow

    def get_queryset(self):
        return UserFollow.objects.filter(user=self.request.user)

class CreateSubscriptionView(FormView):
    model = UserFollow
    fields = ['followed_user']
    success_url = '/subscriptions/'
    template_name = 'subscriptions.html'
    form_class = SubscriptionForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            following_user_name = form.cleaned_data.get('followed_user')
            try:
                target = User.objects.get(username=following_user_name)
            except User.DoesNotExist:
                pass
            else: 
                if request.user.is_authenticated:
                    try:
                        UserFollow.objects.create(user=request.user, followed_user=target)
                    except Exception:
                        pass

        return redirect(self.success_url)

class DeleteSubscriptionView(DeleteView):
    model = UserFollow
    template_name = 'subscriptions.html'
    success_url = '/subscriptions/'

    def post(self, request, *args, **kwargs):
        subscription = self.get_object()
        if subscription.user != request.user:
            return redirect("subscriptions")
        return super().post(request, args, kwargs)
