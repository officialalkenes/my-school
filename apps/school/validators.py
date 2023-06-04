import re

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, RegexValidator


def validate_geeks_mail(value):
    if "@gmail.com" in value:
        return value
    else:
        raise BaseValidator("This field accepts mail id of google only")


def validate_alphabetical(value):
    if not re.search(r"^[a-zA-Z\s]*$", value):
        raise ValidationError("Only alphabetical characters are allowed")


def validate_lower_alphabetical(value):
    if not re.search(r"^[a-zA-Z\s]*$", value):
        raise ValidationError("Only lower case characters are allowed")


"""
Break Day Shuffler
"""
