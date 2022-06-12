from .models import FaceDescriptionsModel
from ..default.models import User
from ..tele_cod.models import TelegramBotModel
from ..default.validators import validate_letters, pass_gen
from .get_face_descriptor import get_descriptor

from django.utils.translation import gettext_lazy as _
from scipy.spatial import distance
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
# from trench.utils import UserTokenGenerator
from ..tele_cod.custom_token import CustomUserTokenGenerator
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

custom_user_tele_token_generator = CustomUserTokenGenerator()


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceDescriptionsModel
        fields = ('photo',)


class ThirdFactorRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    first_name = serializers.CharField(validators=[validate_letters])
    last_name = serializers.CharField(validators=[validate_letters])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    facedescriptionsmodel = PhotoSerializer()

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'facedescriptionsmodel')
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

        try:
            face_descriptor = get_descriptor(validated_data['facedescriptionsmodel']['photo'])
        except Exception:
            raise serializers.ValidationError({'authorisation error': 'Face not recognized'})

        user_face = FaceDescriptionsModel.objects.create(user=user,
                                                         description=face_descriptor)

        user_face.save()

        return user


class CustomFaceAuthObtainSerializer(serializers.Serializer):
    token_class = None

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["ephemeral_token"] = serializers.CharField()
        self.fields["photo"] = serializers.ImageField()

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class CustomFaceAuthObtainPairSerializer(CustomFaceAuthObtainSerializer):
    token_class = RefreshToken
    method = None

    def validate(self, attrs, *args):
        data = {}
        refresh = self.get_token(args[0].user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, args[0].user)

        return data


class FaceAuthrSerializer(CustomFaceAuthObtainPairSerializer):
    method = 'face auth'

    def validate(self, attrs, *args):
        credentials = {
            'ephemeral_token': attrs.get("ephemeral_token"),
            'photo': attrs.get("photo"),
        }
        user_tele_object = custom_user_tele_token_generator.check_token(user=None, token=credentials['ephemeral_token'])

        if user_tele_object is None:
            raise serializers.ValidationError(
                {'authorisation Error': 'Invalid token'}
            )
        try:
            face_desc_incoming = get_descriptor(credentials['photo'])
        except Exception:
            raise serializers.ValidationError({'authorisation error': 'Face not recognized'})

        face_desc_user = FaceDescriptionsModel.objects.filter(user=user_tele_object.user).first()
        euclid_value = distance.euclidean(face_desc_incoming, face_desc_user.description)

        if euclid_value > 0.551:
            raise serializers.ValidationError(
                {'authorisation error': 'You have not been authorized by face'}
            )

        return super().validate(credentials, user_tele_object)
