from django.contrib.auth import get_user_model
from django.db import models

from ads.models import Ad

User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["ad"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"Review by {self.author} on Ad #{self.ad_id}"
