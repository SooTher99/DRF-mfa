from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from trench.utils import UserTokenGenerator

user_token_generator = UserTokenGenerator()


class SecondFactorSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["ephemeral_token"] = serializers.CharField()

    def validate(self, attrs):
        credentials = {
            'ephemeral_token': attrs.get("ephemeral_token"),
            'email': attrs.get("email"),
            'password': attrs.get("password")
        }

        user = user_token_generator.check_token(user=None, token=credentials['ephemeral_token'])
        if user is None:
            raise serializers.ValidationError(
                {'authorisation Error': 'Invalid token'}
            )

        user = authenticate(username=credentials['email'], password=credentials['password'])

        if user is None:
            raise serializers.ValidationError(
                {'authorisation Error': 'Wrong login or password'}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {'authorisation Error': 'Wrong login or password'}
            )

        return super().validate(credentials)
