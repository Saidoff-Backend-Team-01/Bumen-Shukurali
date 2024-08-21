import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_instagram_url(value):
    regex = re.compile(r"^(https?://)?(www\.)?instagram\.com/[a-zA-Z0-9(_)?]+/?$")

    if not regex.match(value):
        raise ValidationError("Enter a valid Instagram URL.")


def validate_telegram_url(value):
    regex = re.compile(r"^(https?://)?(www\.)?t\.me/[a-zA-Z0-9(_)?]+/?$")

    if not regex.match(value):
        raise ValidationError("Enter a valid Telegram URL.")


def phone_number_validator(value):
    regex = re.compile(r"^998[012345789][0-9]{8}$")
    if not regex.match(value):
        raise ValidationError("Enter a valid phone number.")
