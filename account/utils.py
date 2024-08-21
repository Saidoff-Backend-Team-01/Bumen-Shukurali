import secrets

from django.conf import settings
from django.core.mail import send_mail


def generate_otp_code():
    numbers = "0123456789"
    return "".join(secrets.choice(numbers) for _ in range(6))


def send_verification_code(email, code):
    subject = "Verification code"
    message = f"Your activation code is {code}"
    send_mail(
        subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email]
    )
