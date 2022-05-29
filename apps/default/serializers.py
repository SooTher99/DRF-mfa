from django.contrib.auth import authenticate,  get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from .models import User
from ..tele_cod.models import TelegramBotModel
from rest_framework import serializers
from .validators import validate_letters, pass_gen
from trench.utils import UserTokenGenerator
from ..tele_cod.tgbot.bot import bot

user_token_generator = UserTokenGenerator()


class DefaultRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    first_name = serializers.CharField(validators=[validate_letters])
    last_name = serializers.CharField(validators=[validate_letters])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class TwoFactorRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    first_name = serializers.CharField(validators=[validate_letters])
    last_name = serializers.CharField(validators=[validate_letters])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        user_messenger = TelegramBotModel.objects.create(user=user, user_activation_key=pass_gen(8))
        user_messenger.save()

        return user


class DefaultFactorSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'email': attrs.get("email"),
            'password': attrs.get("password")
        }

        user = authenticate(username=credentials['email'], password=credentials['password'])

        if user is None:
            raise serializers.ValidationError(
                {'authorisation error': 'Wrong login or password'}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {'authorisation error': 'Account is not active'}
            )

        return super().validate(credentials)


class CustomTokenObtainSerializer(TokenObtainSerializer):
    def get_token(cls, user):
        return cls.token_class.make_token(user)


class TokenObtainSingleSerializer(CustomTokenObtainSerializer):
    token_class = user_token_generator
    method = None

    def validate(self, attrs):
        data = super().validate(attrs)

        ephemeral_token = self.get_token(self.user)

        data["Ephemeral token"] = ephemeral_token
        data["Method"] = self.method

        return data


class FirstFactorSerializer(TokenObtainSingleSerializer):
    method = 'default auth'
    def validate(self, attrs):
        credentials = {
            'email': attrs.get("email"),
            'password': attrs.get("password")
        }

        user = authenticate(username=credentials['email'], password=credentials['password'])

        if user is None:
            raise serializers.ValidationError(
                {'authorisation Error': 'Wrong login or password'}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {'authorisation Error': 'Account is not active'}
            )

        if not user.telegrambotmodel.user_id_messenger:
            raise serializers.ValidationError(
                {'authorisation Error': 'You are not logged in to the bot'}
            )
        code = pass_gen(8, letters=False)
        user.telegrambotmodel.code = code
        user.save()
        print('#################', code, user.telegrambotmodel.code)
        bot.send_message(chat_id=user.telegrambotmodel.user_id_messenger, text=code)

        return super().validate(credentials)
