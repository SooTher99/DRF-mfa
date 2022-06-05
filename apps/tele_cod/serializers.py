from rest_framework import serializers
from trench.utils import UserTokenGenerator
from django.utils.translation import gettext_lazy as _
from .models import TelegramBotModel
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

user_token_generator = UserTokenGenerator()


def get_code_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_CODE_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed"
            % settings.AUTH_USER_MODEL
        )


class CustomTelegramTokenObtainSerializer(serializers.Serializer):
    code_field = get_code_model().CODE_FIELD
    token_class = None

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["ephemeral_token"] = serializers.CharField()
        self.fields[self.code_field] = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        return cls.token_class.make_token(user)


class CustomTelegramTokenObtainPairSerializer(CustomTelegramTokenObtainSerializer):
    token_class = user_token_generator
    method = None

    def validate(self, attrs, *args):
        data = {}
        ephemeral_token = self.get_token(args[0].user)

        data["Ephemeral token"] = ephemeral_token
        data["Method"] = self.method

        return data


class SecondFactorSerializer(CustomTelegramTokenObtainPairSerializer):
    method = 'code auth'

    def validate(self, attrs, *args):
        credentials = {
            'ephemeral_token': attrs.get("ephemeral_token"),
            'code': attrs.get("code"),
        }
        user_object = user_token_generator.check_token(user=None, token=credentials['ephemeral_token'])

        if user_object is None:
            raise serializers.ValidationError(
                {'authorisation Error': 'Invalid token'}
            )

        user = TelegramBotModel.objects.filter(code=credentials['code'], user=user_object.pk).first()

        if user is None:
            raise serializers.ValidationError(
                {'authorisation Error': 'Wrong code'}
            )

        if not user.user_id_messenger:
            raise serializers.ValidationError(
                {'authorisation Error': 'You are not logged in to the bot'}
            )

        user.code = None
        user.save()

        return super().validate(credentials, user)
