from django.conf import settings
from django.core.mail import send_mail


def send_reset_password_email(to_email, reset_link) -> None:
    """Sends email with instructions to reset password to given email address."""

    subject = "Password Reset"
    message = f"To reset your password follow the link: {reset_link}"

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
