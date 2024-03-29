from .models import User

from rest_framework.serializers import ValidationError
from string import punctuation, digits, ascii_uppercase
import random


def validate_letters(name):
    if not set(name).isdisjoint(punctuation + digits):
        raise ValidationError({"incorrect name": "Name must contain only letters"})
    elif not name[0].isupper():
        raise ValidationError({"incorrect name": "Name must start with a capital letter"})


def pass_gen(length, numbers=True, letters=True):
    password = ''
    for i in range(0, length // 2):
        if numbers:
            password += random.choice(digits)
        if letters:
            password += random.choice(ascii_uppercase)
    return password


def get_user_activation_key(user_email):
    user = User.objects.filter(email=user_email).first()
    return user.telegrambotmodel.user_activation_key
