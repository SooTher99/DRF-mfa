from .serializers import SecondFactorSerializer, TwoFactorRegisterSerializer
from ..default.validators import get_user_activation_key

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class RegisterApiForTwoFactors(GenericAPIView):
    serializer_class = TwoFactorRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "User Created Successfully. Now perform Login to get your token",
            "your activation key in the bot": get_user_activation_key(serializer.data.get('email')),
        }, status=status.HTTP_201_CREATED)


class MFASecondStepJWTView(TokenObtainPairView):
    serializer_class = SecondFactorSerializer
