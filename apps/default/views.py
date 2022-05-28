from rest_framework.generics import GenericAPIView
from .serializers import TwoFactorRegisterSerializer, FirstFactorSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .validators import get_user_activation_key
from trench.views.jwt import MFAJWTView
from django.contrib.auth.models import User
from abc import ABC, abstractmethod
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from trench.backends.provider import get_mfa_handler
from trench.command.authenticate_user import authenticate_user_command
from trench.exceptions import MFAMethodDoesNotExistError, MFAValidationError
from trench.responses import ErrorResponse
from trench.serializers import (
    LoginSerializer,
)
from trench.utils import get_mfa_model, user_token_generator


class RegisterApi(GenericAPIView):
    serializer_class = TwoFactorRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "User Created Successfully. Now perform Login to get your token",
            "your activation key in the bot": get_user_activation_key(serializer.data.get('email')),
        })


class MFAFirstStepJWTView(TokenObtainPairView):
    serializer_class = FirstFactorSerializer


# class MFAStepMixin(GenericAPIView, ABC):
#     permission_classes = (AllowAny,)
#
#     @abstractmethod
#     def _successful_authentication_response(self, user: User) -> Response:
#         raise NotImplementedError
#
#
# class MFAFirstStepMixin(MFAStepMixin, ABC):
#     def post(self, request: Request) -> Response:
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             user = authenticate_user_command(
#                 request=request,
#                 username=serializer.validated_data[User.USERNAME_FIELD],
#                 password=serializer.validated_data["password"],
#             )
#         except MFAValidationError as cause:
#             return ErrorResponse(error=cause)
#         try:
#             mfa_model = get_mfa_model()
#             mfa_method = mfa_model.objects.get_primary_active(user_id=user.id)
#             get_mfa_handler(mfa_method=mfa_method).dispatch_message()
#             return Response(
#                 data={
#                     "ephemeral_token": user_token_generator.make_token(user),
#                     "method": mfa_method.name,
#                 }
#             )
#         except MFAMethodDoesNotExistError:
#             return self._successful_authentication_response(user=user)
#
#
# class MFAFirstStepJWTView(MFAJWTView, MFAFirstStepMixin):
#     serializer_class = LoginSerializer
