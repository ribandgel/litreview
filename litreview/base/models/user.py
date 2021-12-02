from django.db import models
from django.contrib.auth import get_user_model

class UserFollow(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="followed_by")

    class Meta:
        app_label = "base"
        unique_together = ("user", "followed_user")