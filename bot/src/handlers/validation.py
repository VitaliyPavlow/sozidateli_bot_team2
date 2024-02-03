import re

from aiogram_forms.errors import ValidationError
from email_validator import EmailNotValidError, validate_email

from .constants import (INVALID_EMAIL_MESSAGE, INVALID_PHONE_NUMBER_MESSAGE,
                        INVALID_VOLUNTEERING_TYPE_MESSAGE, NUMBER_PATTERN,
                        VOLUNTEERING_TYPE)


def validate_email_format(value: str):
    """Email validator."""
    try:
        validate_email(value, check_deliverability=False)
    except EmailNotValidError:
        raise ValidationError(INVALID_EMAIL_MESSAGE, code='email')


def validate_phone_number_format(value: str):
    """Phone number validator."""
    if not re.match(NUMBER_PATTERN, value):
        raise ValidationError(
            INVALID_PHONE_NUMBER_MESSAGE, code='phone_number'
        )


def validate_volunteering_type_field(value: str):
    """Volunteering type validator."""
    if value not in tuple(map(lambda x: x[1], VOLUNTEERING_TYPE)):
        raise ValidationError(
            INVALID_VOLUNTEERING_TYPE_MESSAGE, code='volunteering_type'
        )
