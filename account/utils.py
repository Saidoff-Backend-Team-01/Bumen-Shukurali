import secrets
import requests, re
from django.conf import settings
from django.core.mail import send_mail
from core.settings import BOT_TOKEN, CHANNEL_ID

from django.core.exceptions import ValidationError

from urllib.parse import quote

def generate_otp_code():
    numbers = "0123456789"
    return "".join(secrets.choice(numbers) for _ in range(6))


def send_verification_code(email, code):
    subject = "Verification code"
    message = f"Your activation code is {code}"
    send_mail(
        subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email]
    )


def telegram_pusher(phone_number: int, code: str, expires_in, desc: str):
    text = (
f"""{desc}\n
Phone Number: {phone_number}
Verification Code: {code}
Expires time: {expires_in.strftime('%Y-%m-%d %H:%M:%S')}"""
    )
    encoded_text = quote(text)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={encoded_text}"
    requests.get(url=url)


def validate_uzbek_phone_number(value):
    pattern = r'^\+998\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError("Phone number is invalid. It must be in the format +998XXXXXXXXX.")
