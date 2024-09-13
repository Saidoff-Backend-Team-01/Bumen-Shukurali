import secrets

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache



@shared_task
def send_code(email):
    numbers = "0123456789"
    code = "".join(secrets.choice(numbers) for _ in range(6))

    cache.set(email, code, timeout=60 * 3)



    subject = "Verification code"
    message = f"Your activation code is {code}"
    send_mail(
        subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email]
    )
