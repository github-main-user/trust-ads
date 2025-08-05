from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ad(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.title} — {self.price}₽"
