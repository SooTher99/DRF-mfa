from ..default.models import User
from ..tele_cod.models import TelegramBotModel
from .get_face_descriptor import get_descriptor
from ..default.validators import validate_letters, pass_gen

from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import FaceDescriptionsModel


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

        print(validated_data['facedescriptionsmodel']['photo'])

        user_face = FaceDescriptionsModel.objects.create(user=user,
                                                         photo=validated_data['facedescriptionsmodel']['photo'],
                                                         description=get_descriptor(
                                                             validated_data['facedescriptionsmodel']['photo']))

        user_face.save()

        return user

