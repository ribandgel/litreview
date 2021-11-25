from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="tickets")
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "app"

class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(max_length=1024, validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "app"