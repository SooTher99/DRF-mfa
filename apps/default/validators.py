from rest_framework.serializers import ValidationError
from string import punctuation, digits, ascii_uppercase
import random


def validate_letters(name):
    if not set(name).isdisjoint(punctuation + digits):
        raise ValidationError({"incorrect name": "Name must contain only letters"})
    elif not name[0].isupper():
        raise ValidationError({"incorrect name": "Name must start with a capital letter"})


def pass_gen(length):
    password = ''
    for i in range(0, length//2):
        password += random.choice(digits)
        password += random.choice(ascii_uppercase)
    return password