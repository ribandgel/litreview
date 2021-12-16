from django import forms

class SubscriptionForm(forms.Form):
    followed_user = forms.CharField()
