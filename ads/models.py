from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ad(models.Model):
    """Represents an advertisement."""

    title = models.CharField(max_length=255, help_text="The title of the ad.")
    price = models.PositiveIntegerField(help_text="The price of the ad (in RUR).")
    description = models.TextField(help_text="A detailed description of the ad.")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ads",
        help_text="The user who created the ad.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the ad was created."
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["created_at"]),
        ]
        verbose_name = "Ad"
        verbose_name_plural = "Ads"

    def __str__(self) -> str:
        return f"{self.title} — {self.price}₽"
