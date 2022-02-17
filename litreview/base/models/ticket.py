from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import RATING_CHOICES
from .user import User


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    image = models.ImageField(null=True, blank=True, upload_to="images")
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "base"


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], choices=RATING_CHOICES
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "base"
