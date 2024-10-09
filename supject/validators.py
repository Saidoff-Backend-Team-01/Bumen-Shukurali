import re

from django.utils import timezone
from django.core.exceptions import ValidationError


def card_number_validator(value):
    if not re.match(r'^\d{16}$', value):
        raise ValidationError("Enter a valid phone number.")


def expiry_date_validator(value):
    if not re.match(r'^\d{2}/\d{2}$', value):
        raise ValidationError("Enter a valid phone number.")

    month, year = map(int, value.split('/'))
    current_year = timezone.now().year % 100
    current_month = timezone.now().month

    if (year < current_year) or (year == current_year and month < current_month):
        raise ValidationError('Karta muddati utgan.')

