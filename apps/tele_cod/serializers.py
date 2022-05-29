from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions
from trench.utils import UserTokenGenerator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import update_last_login
from rest_framework.settings import api_settings
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

    def validate(self, attrs):
        authenticate_kwargs = {
            self.code_field: attrs[self.code_field],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # if not api_settings.USER_AUTHENTICATION_RULE(self.user):
        #     raise exceptions.AuthenticationFailed(
        #         self.error_messages["no_active_account"],
        #         "no_active_account",
        #     )

        return {}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.make_token(user)


class CustomTelegramTokenObtainPairSerializer(CustomTelegramTokenObtainSerializer):
    token_class = user_token_generator
    method = None

    def validate(self, attrs):
        data = super().validate(attrs)

        ephemeral_token = self.get_token(self.user)

        data["Ephemeral token"] = ephemeral_token
        data["Method"] = self.method

        return data


class SecondFactorSerializer(CustomTelegramTokenObtainPairSerializer):
    method = 'code auth'

    def validate(self, attrs):
        credentials = {
            'ephemeral_token': attrs.get("ephemeral_token"),
            'code': attrs.get("code"),
        }
        user = user_token_generator.check_token(user=None, token=credentials['ephemeral_token'])

        if user is None:
            raise serializers.ValidationError(
                {'authorisation Error': 'Invalid token'}
            )

        user = authenticate(code=credentials['code'])
        user = TelegramBotModel.objects.filter(code=credentials['code'], user=user.pk).first()

        if user is None:
            raise serializers.ValidationError(
                {'authorisation Error': 'Wrong code'}
            )

        if not user.user_id_messenger:
            raise serializers.ValidationError(
                {'authorisation Error': 'You are not logged in to the bot'}
            )

        return super().validate(credentials)
