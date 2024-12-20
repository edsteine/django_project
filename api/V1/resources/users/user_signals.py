from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender: type[Model], instance: User, created: bool, **kwargs: dict[str, Any]) -> None:
    """Send a welcome email to the newly created user.

    Args:
        sender (type[Model]): The model class that triggered the signal.
        instance (User): The instance of the created user.
        created (bool): Whether the instance is newly created.
        **kwargs: Additional keyword arguments passed by the signal.
    """
    if created:
        subject = "Welcome to Our Platform"
        message = f"Hello {instance.first_name},\n\nWelcome to our platform! We are excited to have you on board."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)
