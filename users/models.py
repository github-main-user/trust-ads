from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .managers import UserManager

phone_validator = RegexValidator(
    regex=r"^\+?\d{9,15}$",
    message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed.",
)


class User(AbstractUser):
    class UserRole(models.TextChoices):
        USER = "User", "user"
        ADMIN = "Admin", "admin"

    username = None

    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15, validators=[phone_validator], blank=True, null=True
    )
    role = models.CharField(
        max_length=5, choices=UserRole.choices, default=UserRole.USER
    )
    image = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: UserManager = UserManager()

    class Meta:
        indexes = [models.Index(fields=["role"])]

    def __str__(self) -> str:
        return self.email

    def is_admin(self) -> bool:
        return self.role == self.UserRole.ADMIN
