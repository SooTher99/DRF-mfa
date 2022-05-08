from rest_framework.serializers import ValidationError
from string import punctuation, digits


def validate_letters(name):
    if not set(name).isdisjoint(punctuation + digits):
        raise ValidationError({"incorrect name": "Name must contain only letters"})
    elif not name[0].isupper():
        raise ValidationError({"incorrect name": "Name must start with a capital letter"})
